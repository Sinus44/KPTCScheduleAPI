from fastapi import APIRouter

import src.config as config
from src.http_exceptions import FileNotFoundException, InvalidParameterException
from src.schemes.exception_response import ExceptionResponse
from src.schemes.file_response import FileResponse
from src.schemes.files_response import FilesResponse
from src.services.file_service import FileService
from src.validator import validate_file_id, validate_date

file_controller = FileService(config.FILE_CONTROLLER_CONFIG.get("folder_id"))
file_router = APIRouter(prefix="/file", tags=["file"])


@file_router.get("/getAll", summary="Получить все файлы")
def file_get_all() -> FilesResponse:
    return FilesResponse(files=[file.serialize() for file in file_controller.get_available_files()])


@file_router.get("/getActual", summary="Получить только актуальные файлы")
def file_get_actual() -> FilesResponse:
    return FilesResponse(files=[file.serialize() for file in file_controller.get_actual_files()])


@file_router.get("/getById", summary="Получить файл по ID", responses={
    400: {"model": ExceptionResponse, "description": "Invalid file_id"},
    404: {"model": ExceptionResponse, "description": "File not found"},
})
def file_get_by_id(file_id: str) -> FileResponse:
    file_id = validate_file_id(file_id)

    if file_id is None:
        raise InvalidParameterException("file_id")

    file = file_controller.get_file_by_id(file_id)

    if file is None:
        raise FileNotFoundException

    return file.serialize()


@file_router.get("/getByDate", summary="Получить файл по дате", responses={
    400: {"model": ExceptionResponse, "description": "Invalid date"},
    404: {"model": ExceptionResponse, "description": "File not found"},
})
def file_get_by_date(date: str) -> FileResponse:
    date = validate_date(date)

    if date is None:
        raise InvalidParameterException("date")

    file = file_controller.get_file_by_date(date)

    if file is None:
        raise FileNotFoundException

    return file.serialize()
