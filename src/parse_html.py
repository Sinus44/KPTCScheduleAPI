import logging
from collections import defaultdict

import lxml.html
import requests

from src.datatypes.group import Group
from src.datatypes.lesson import Lesson
from src.validator import parse_group_name


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda: defaultdict())

    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()

            while row_i in result and col_i in result[row_i]:
                col_i += 1

            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


def get_raw_html_table_content(content):
    res = []

    for table_el in lxml.html.fromstring(content).xpath('//table'):
        res.append(table_to_list(table_el))

    return sum(res, [])


def get_raw_html_table_filename(file_path):
    res = []

    for table_el in lxml.html.parse(file_path).xpath('//table'):
        res.append(table_to_list(table_el))

    return sum(res, [])


def remove_repeats(string, symbol):
    """Remove all repeats symbols"""
    while (symbol * 2) in string:
        string = string.replace(symbol * 2, symbol)

    return string


def split_into_chunks_smart(array):
    arr = []

    for string in array:
        cabinet_in_str = "каб" in string

        if cabinet_in_str:
            arr.append([])

        arr[-1].append(string)

    return arr


def split_matrix(matrix, split_column):
    """Функция для деления двумерного массива (матрицы) на 2 матрицы по столбцам"""
    left_matrix = [row[:split_column] for row in matrix]
    right_matrix = [row[split_column:] for row in matrix]
    return left_matrix, right_matrix


def get_html(file_id):
    return requests.get(f"https://docs.google.com/document/u/0/export?format=html&id={file_id}").text


def parse_html(file_id):
    """Main function for parse schedule html file"""
    logging.info(f"Парсинг фалйа {file_id}")

    # Список для хранения групп
    groups = []
    content = get_html(file_id)
    data = get_raw_html_table_content(content)

    data_new = []

    for line in data:
        new_line = []

        for i, elem in enumerate(line):
            # Для 3го столбца роспы сносим продублированное
            if len(line) == 10 and i == 7:
                continue

            new_line.append(elem.replace("\xa0", "")
                            .replace("\n", "")
                            .replace("\r", "")
                            .replace("\t", "")
                            .replace("—", "-"))

        data_new.append(new_line)

    data = data_new

    # Массив строк групп (ранее 5 строчные матрицы)
    chunks = split_into_chunks_smart(data)
    for i, chunk in enumerate(chunks):
        # Изначально - первая матрицы - это текущий правый "кусок"
        split_right = chunk

        # 3 раза делим (потому что максимум 3 группы в строке)
        for _ in range(3):
            # Делим матрицу из 5 строк и 9 столбцов НА 3 матрицы размерами 3 на 5
            split_left, split_right = split_matrix(split_right, 3)

            # Если группа (текущий левый "кусок") пустая, то не добавляем ее в список групп
            if split_left == [[], [], [], [], []]:
                continue

            # Добавляем группу в список групп
            groups.append(split_left)

    # Список групп (уже как объектов, а не списков)
    groups_obj = []

    # Для каждой группы
    for group in groups:
        # Создаем экземпляр группы

        # Получаем имя группы
        group_name = group[0][0].replace(" ", "")

        # Группа без имени - плохая группа
        if group_name == "":
            # Пропускаем её к чертям собачьим
            continue

        group_name_match = parse_group_name(group_name)

        if not group_name_match["valid"]:
            logging.error(f"Ошибка обработки группы {group_name}")
            continue

        parsed_group = Group()
        parsed_group.course = int(group_name_match["course"])
        parsed_group.sub_group = int(group_name_match["subgroup"])
        parsed_group.spec = group_name_match["char"]
        parsed_group.school_year = int(group_name_match["year"])
        parsed_group.name = group_name_match["full_name"]

        prev_lesson = None
        # Для каждого занятия группы (с первого индекса, так как нулевой это заголовок таблички)
        for lesson in group[1:]:
            # Если у занятия почему-то не 3 параметра (номер пары, дисциплина, кабинет), то...
            if len(lesson) < 3:
                # Пропускаем это занятие
                continue

            # lesson = [part.strip() for part in lesson]

            # Если нет пары, то...
            lesson[1] = lesson[1].strip()
            if lesson[1] == "":
                # Пропускаем это занятие
                continue

            discipline = remove_repeats(lesson[1], '-')

            if discipline == "-":
                continue

            # Создаем экземпляр занятия
            parsed_lesson = Lesson()
            parsed_lesson.index = int(lesson[0]) if lesson[0] and lesson[0].isdigit else parsed_group.lessons[-1].index + 1

            parsed_lesson.discipline = time_parser(discipline)
            parsed_lesson.classroom_raw = remove_repeats(lesson[2].replace("—", "-"), "-")

            if parsed_lesson.classroom_raw == "" and parsed_lesson.discipline != "" \
                    and parsed_lesson.discipline.lower() != "физкультура" and len(parsed_group.lessons) != 0:
                parsed_lesson.classroom_raw = parsed_group.lessons[-1].classroom_raw

            if len(parsed_lesson.classroom_raw):
                if parsed_lesson.classroom_raw[-1] == "/":
                    parsed_lesson.classroom_raw = parsed_lesson.classroom_raw[:-1]

                if parsed_lesson.classroom_raw[0] == "/":
                    parsed_lesson.classroom_raw = parsed_lesson.classroom_raw[1:]

            if parsed_lesson.classroom_raw == "-":
                parsed_lesson.classroom_raw = ""

            if (parsed_lesson.classroom_raw == "ср" or parsed_lesson.classroom_raw == "экс" or
                    parsed_lesson.classroom_raw == ""):
                parsed_lesson.postfix = ""

            else:
                parsed_lesson.postfix = "каб."

            if parsed_lesson.postfix == "" and parsed_lesson.classroom_raw == "":
                parsed_lesson.classroom = ""
            else:
                parsed_lesson.classroom = f"{parsed_lesson.classroom_raw} {parsed_lesson.postfix}".strip()

            if prev_lesson:
                if parsed_lesson.discipline == prev_lesson.classroom:
                    parsed_lesson.discipline = prev_lesson.discipline
                    parsed_lesson.classroom = prev_lesson.classroom

            prev_lesson = parsed_lesson

            # Добавляем занятие в список занятий группы
            parsed_group.lessons.append(parsed_lesson)

        # Добавляем группу в список
        groups_obj.append(parsed_group)

    # Возвращаем список групп
    logging.info(f"Файл {file_id} успешно спарсили")
    return groups_obj


def time_parser(discipline_name):
    discipline_name = discipline_name.replace("(", " (")
    split = discipline_name.split()

    for i, part in enumerate(split):
        is_digit = part.isdigit()

        if not is_digit:
            continue

        if len(part) == 3:
            split[i] = part[0] + ":" + part[1:]

        elif len(part) == 4:
            split[i] = part[:2] + ":" + part[2:]

    return remove_repeats(" ".join(split), " ")
