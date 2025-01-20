"""Module for parsing Google Folder"""
import datetime
import logging
import os
import re
import time

import bs4
import requests
import urllib3

from src.datatypes.google_file import GoogleFile
from src.datatypes.google_folder import GoogleFolder
from src.datatypes.schedule_file import File
from src.enums.weekday_name import get_weekday_name_by_index

MONTHS = {
    'янв': 1,
    'февр': 2,
    'мар': 3,
    'апр': 4,
    'мая': 5,
    'июн': 6,
    'июл': 7,
    'авг': 8,
    'сент': 9,
    'окт': 10,
    'нояб': 11,
    'дек': 12
}

MONTHS_FULL = {
    'январь': 1,
    'февраль': 2,
    'март': 3,
    'апрель': 4,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12
}


class IncorrectStatusCode(Exception):
    def __init__(self, code=404):
        Exception.__init__(self, f"Incorrect status code is {code}")


class NotFoundOnDrive(Exception):
    def __init__(self):
        Exception.__init__(self, "Not found on drive")


def parse_folder_name(folder_name):
    if " " in folder_name:
        month_name, year_str = folder_name.split(" ")

        month = MONTHS_FULL.get(month_name.lower())
        year = int(year_str)
        return month, year

    return 0, 0


def parse_file_name(full_file_name):
    file_name, _ = os.path.splitext(full_file_name)
    file_day, _ = file_name.split(" ")

    if file_day.isdigit():
        return int(file_day), file_name

    return 0, file_name


def request(google_id) -> str:
    html_content = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html"
    }

    url = f"https://drive.google.com/drive/folders/{google_id}"

    while not html_content:
        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                raise IncorrectStatusCode(response.status_code)

        except requests.exceptions.ConnectTimeout:
            logging.error("Вышло время подключения")

        except (requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError):
            logging.error("Вышло время чтения")

        except requests.exceptions.ConnectionError:
            logging.error("Ошибка подключения")

        except IncorrectStatusCode as e:
            logging.error("Ошибка запроса к гугл диску, неправильный статус код ошибки")
            logging.error(e)

        except Exception as e:
            logging.error("Exception", e)
            logging.exception("Unknown error")

        else:
            html_content = response.text
            break

        logging.warning("Повтор запроса")
        time.sleep(3)

    return html_content


def parse_google_folder(google_folder: GoogleFolder):
    return parse_google_items(google_folder)


def parse_google_items(folder: GoogleFolder) -> list:
    html_content = request(folder.id)

    soup = bs4.BeautifulSoup(html_content, "html.parser")
    div_list = soup.findAll("div", {'class': "iZmuQc"})

    if len(div_list) < 1:
        # Special for debugging
        # with open("special_for_debug.html", "w", encoding="utf-8") as file:
        #    file.write(html_content)

        raise NotFoundOnDrive

    files_div = div_list[0].findAll("div", {'data-target': "doc"})
    items = []

    for item_div in files_div:
        google_id = item_div["data-id"]
        google_name = item_div.find("div", {"class": "KL4NAf"}).text

        is_folder = False
        type_f = item_div.findAll("div", {'class': "l-o-c-qd"})

        if type_f:
            is_folder = type_f[0]["aria-label"] == "Google Drive Folder с общим доступом."

        if is_folder:
            google_folder = GoogleFolder()
            google_folder.id = google_id
            google_folder.name = google_name
            google_folder.element = item_div

            items.append(google_folder)

        else:
            google_file = GoogleFile()
            google_file.id = google_id
            google_file.last_update = get_file_update(item_div)
            google_file.name = google_name

            items.append(google_file)

    return items


def get_file_update(element):
    """Вытягиваем время / дату обновления файла из HTML элемента этого файла"""
    last_update_str = element.find("span", {"class": "jApF8d"}).text.replace("\u202fг.", "").replace(" ", '.')
    last_update = 0

    if re.compile(r"\d{1,2}:\d{1,2}").match(last_update_str):
        today = datetime.datetime.now()

        now_time = today.time()
        file_time = datetime.datetime.strptime(last_update_str, '%H:%M').time()

        if now_time > file_time:
            # Файл обновлен сегодня
            now_str = today.strftime("%d.%m.%Y ")
        else:
            yesterday = today - datetime.timedelta(days=1)
            # Файл обновлен вчера
            now_str = yesterday.strftime("%d.%m.%Y ")

        full_date = now_str + last_update_str
        last_update = datetime.datetime.strptime(full_date, '%d.%m.%Y %H:%M').timestamp()

    elif match := re.compile(r'(\d{1,2}).(\w+).?.(\d{4})').match(last_update_str):
        full_date = f"{match[1]}.{MONTHS[match[2]]}.{match[3]}"
        last_update = datetime.datetime.strptime(full_date, '%d.%m.%Y').timestamp()

    return int(last_update)


def get_weekday_index(date: str):
    date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    return date_obj.weekday()


def convert_to_schedule_file(google_folder, google_file):
    month, year = parse_folder_name(google_folder.name)
    day, name = parse_file_name(google_file.name)
    date = f"{day}.{month}.{year}"
    weekday_index = get_weekday_index(date)

    schedule_file = File()
    schedule_file.name = name
    schedule_file.date = date
    schedule_file.last_update = google_file.last_update
    schedule_file.full_name = google_file.name
    schedule_file.id = google_file.id
    schedule_file.weekday_index = weekday_index
    schedule_file.week_day_name = get_weekday_name_by_index(weekday_index)
    schedule_file.day = day

    return schedule_file


def parse_all(root_folder_id) -> list | None:
    google_folder = GoogleFolder()
    google_folder.id = root_folder_id

    sub_folders = parse_google_folder(google_folder)

    if sub_folders is None:
        raise NotFoundOnDrive

    schedule_files = []

    for sub_folder in sub_folders:
        files = parse_google_folder(sub_folder)

        if files is None:
            raise NotFoundOnDrive

        for file in files:
            schedule_file = convert_to_schedule_file(sub_folder, file)
            schedule_files.append(schedule_file)

    return schedule_files
