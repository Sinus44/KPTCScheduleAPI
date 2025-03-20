import src.parse_folder as parse_folder
from src.datatypes.schedule_file import File
from src.services.check_actual_service import get_actual_from_list


class FileService:
    def __init__(self, folder_id):
        self.folder_id = folder_id
        self.files: list[File] | None = None

    def update_available_files(self) -> list[File]:
        self.files = parse_folder.parse_all(self.folder_id)
        return self.files

    def get_available_files(self) -> list[File]:
        if self.files is None:
            return self.update_available_files()

        return self.files

    def get_actual_files(self) -> list[File]:
        files = self.get_available_files()
        actual_files = get_actual_from_list(files)
        return actual_files

    def get_file_by_date(self, date) -> File | None:
        files = self.get_available_files()
        date = ".".join(map(str, map(int, date.split("."))))
        file = [file for file in files if file.date == date]

        if len(file) > 0:
            return file[0]
        else:
            return None

    def get_file_by_id(self, file_id):
        files = self.get_available_files()
        file = [file for file in files if file.id == file_id]

        if file:
            return file[0]
        else:
            return None
