import logging
import time

from src.converter import convert_list_schedule_to_dict
from src.database import SessionLocal
from src.datatypes.schedule_file import File
from src.enums.fileupdatetype import FileUpdateType
from src.models.file_update_model import FileUpdateModel
from src.models.schedule_update_model import ScheduleUpdateModel
from src.parse_folder import NotFoundOnDrive
from src.services.check_actual_service import get_current_date, check_actual_with_date
from src.services.database_service import create_file_update, create_schedule_update
from src.services.file_service import FileService
from src.services.schedule_service import ScheduleService


def check_outdated(other_ids, new_files, last_files):
    outdated_ids = []
    date = get_current_date()

    for other_id in other_ids:
        last_file = [file for file in last_files if file["id"] == other_id][0]
        new_file = [file for file in new_files if file["id"] == other_id][0]

        last_file_actual = check_actual_with_date(last_file["date"], date)
        new_file_actual = check_actual_with_date(new_file["date"], date)

        if not new_file_actual and last_file_actual:
            outdated_ids.append(other_id)

    return outdated_ids


def check_add_delete(new_ids, last_ids):
    deleted_ids = []
    added_ids = []

    for new_id in new_ids:
        if new_id not in last_ids:
            added_ids.append(new_id)

    for last_id in last_ids:
        if last_id not in new_ids:
            deleted_ids.append(last_id)

    return added_ids, deleted_ids


def check_edited(other_ids, new_files, last_files):
    edited_ids = []

    for other_id in other_ids:
        last_file = [file for file in last_files if file["id"] == other_id][0]
        new_file = [file for file in new_files if file["id"] == other_id][0]

        if new_file["last_update"] > last_file["last_update"]:
            edited_ids.append(other_id)

    return edited_ids


def check_other(all_ids, added_ids, deleted_ids):
    other_ids = []

    for all_id in all_ids:
        if (all_id not in added_ids) and (all_id not in deleted_ids):
            other_ids.append(all_id)

    return other_ids


class UpdateService:
    def __init__(self, file_controller, schedule_controller, update_time=1 * 60):
        self.file_controller: FileService = file_controller
        self.schedule_controller: ScheduleService = schedule_controller
        self.update_time = update_time
        self.last_files: list[dict] | None = None
        self.last_schedule: list[dict] | None = None

    def check(self):
        logging.debug("Update controller checking")
        # TODO: Реализовать overwritten, проверить всё это дело, особенно overwrite после еще одного чека

        try:
            logging.debug("Получение файлов")
            new_files: list[File] = self.file_controller.update_available_files()
            logging.info("Файлы получились")

        except NotFoundOnDrive as e:
            logging.error("Files on google drive not found")
            logging.error(e)
            logging.exception("Not found files on google drive")
            return

        logging.debug("Сериализация файлов")
        new_files_serialized = [file.__dict__ for file in new_files]
        logging.debug("Сериализация файлов закончена")

        if self.last_files is None:
            logging.debug("Похоже это первый запуск")
            self.last_files = new_files_serialized
            logging.debug("Сохранили сериализованые файлы, получаем расписание")
            last_schedule = self.schedule_controller.update_list(new_files)
            logging.debug("Расписание получили, сохраняем..")
            self.last_schedule = convert_list_schedule_to_dict(last_schedule)
            logging.debug("Расписание сохранили, выходим")
            return

        logging.debug("Формируем списки идентификаторов")
        last_ids = [file["id"] for file in self.last_files]
        new_ids = [file["id"] for file in new_files_serialized]
        all_ids = list(set(new_ids + last_ids))
        logging.debug("Сформировали списки идентификаторов, проверяем новые")

        added_ids, deleted_ids = check_add_delete(new_ids, last_ids)
        logging.debug("Проверяем другие")
        other_ids = check_other(all_ids, added_ids, deleted_ids)
        logging.debug("Проверяем не актуальные")
        outdated_ids = check_outdated(other_ids, new_files_serialized, self.last_files)
        logging.debug("Проверяем измененные")
        edited_ids = check_edited(other_ids, new_files_serialized, self.last_files)

        logging.debug("Сохраняем новые, для следующих проверок")
        self.last_files = new_files_serialized

        logging.debug("Формируем массивы файлов, новые")
        added = [self.file_controller.get_file_by_id(fid) for fid in added_ids]
        # other = [self.file_controller.getFileID(fid) for fid in other_ids]
        logging.debug("Не актуальные")
        outdated = [self.file_controller.get_file_by_id(fid) for fid in outdated_ids]
        logging.debug("Изменённые")
        edited = [self.file_controller.get_file_by_id(fid) for fid in edited_ids]

        logging.debug("Проверили")
        file_updates = []
        update_time = int(time.time())

        logging.debug("Формируем модели, добавлено")

        for file in added:
            file_updates.append(FileUpdateModel(
                update_time=update_time,
                update_file_id=file.id,
                update_type=FileUpdateType.ADDED
            ))

        logging.debug("Формируем модели, удалено")
        for file_id in deleted_ids:
            file_updates.append(FileUpdateModel(
                update_time=update_time,
                update_file_id=file_id,
                update_type=FileUpdateType.DELETED
            ))

        logging.debug("Формируем модели, устарело")
        for file in outdated:
            file_updates.append(FileUpdateModel(
                update_time=update_time,
                update_file_id=file.id,
                update_type=FileUpdateType.OUTDATED
            ))

        logging.debug("Формируем модели, изменено")
        for file in edited:
            file_updates.append(FileUpdateModel(
                update_time=update_time,
                update_file_id=file.id,
                update_type=FileUpdateType.EDITED
            ))

        logging.debug("Делаем запрос на измененное и добавленное расписание")
        new_schedule = self.schedule_controller.update_list(edited + added)
        # new_schedule_serialized = [schedule.__dict__ for schedule in new_schedule]
        logging.debug("Сериализация расписания")
        new_schedule_serialized = convert_list_schedule_to_dict(new_schedule)

        schedule_updates = []
        logging.debug("Проверяем, есть ли изменения")
        if edited:
            logging.debug("Изменения есть, ищем что там за группы поменялась")
            schedule_file_updates = []
            check_schedule_files_ids = [file.id for file in edited]

            for eid in check_schedule_files_ids:
                last_groups = [f for f in self.last_schedule if f["file"]["id"] == eid][0]["groups"]
                new_groups = [f for f in new_schedule_serialized if f["file"]["id"] == eid][0]["groups"]

                edited_groups = {}
                for new_group in new_groups:
                    if new_group not in last_groups:
                        if new_group["name"] not in edited_groups:
                            edited_groups[new_group["name"]] = {}

                        edited_groups[new_group["name"]]["new"] = new_group

                for last_group in last_groups:
                    if last_group not in new_groups:
                        if last_group["name"] not in edited_groups:
                            edited_groups[last_group["name"]] = {}

                        edited_groups[last_group["name"]]["old"] = last_group

                if edited_groups:
                    schedule_file_updates.append({
                        "file_id": eid,
                        "group_names": list(edited_groups.keys())
                    })
                logging.debug("Определили что за группы менялись")

            logging.debug("Создаём обновления расписания для БД")
            for update in schedule_file_updates:
                for group_name in update["group_names"]:
                    schedule_updates.append(ScheduleUpdateModel(
                        update_time=update_time,
                        update_file_id=update["file_id"],
                        update_group=group_name,
                    ))

        logging.debug("Сохраняем расписание для следующей итерации")
        self.last_schedule = new_schedule_serialized

        logging.debug("начинаем запись в БД")
        with SessionLocal() as session:
            for file_update in file_updates:
                record = create_file_update(session, file_update)
                logging.debug(f"Обнаружено изменение файла, ID: {record.id}")

            for schedule_update in schedule_updates:
                record = create_schedule_update(session, schedule_update)
                logging.debug(f"Обнаружено изменение расписания, ID: {record.id}")

    def start(self):
        logging.debug("Поток отслеживания изменений расписания и файлов запущен")

        while True:
            logging.info("Запускаем проверку")
            self.check()
            logging.info("Проверку выполнили, спим")
            time.sleep(self.update_time)
            logging.info("Выспались")
