from datetime import datetime, time


def get_current_date() -> datetime:
    return datetime.combine(datetime.now().date(), time())


def check_actual(file_date: str) -> bool:
    return check_actual_with_date(file_date, get_current_date())


def check_actual_with_date(file_date: str, date) -> bool:
    file_time_stamp = datetime.strptime(file_date, "%d.%m.%Y")
    return file_time_stamp >= date


def get_actual_from_list(files: list) -> list:
    actual_files = [file for file in files if check_actual(file.date)]
    return actual_files
