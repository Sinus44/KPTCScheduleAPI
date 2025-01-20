from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.config import FILE_UPDATE_CONFIG
from src.converter import convert_model_to_dto_file_update, convert_model_to_dto_schedule_update
from src.database import get_db
from src.http_exceptions import InvalidParameterException
from src.routers.file_router import file_controller
from src.routers.schedule_router import schedule_controller
from src.schemes.exception_response import ExceptionResponse
from src.schemes.file_update_id_response import UpdateIdResponse
from src.schemes.file_updates_response import FileUpdatesResponse
from src.schemes.schedule_updates_response import ScheduleUpdatesResponse
from src.services.database_service import get_last_file_update_id, get_file_updates_by_offset, get_last_schedule_update_id, get_schedule_updates_by_offset
from src.services.file_update_service import UpdateService

file_update_controller = UpdateService(file_controller, schedule_controller, FILE_UPDATE_CONFIG["update_time_sec"])
callback_router = APIRouter(prefix="/callback", tags=["callback"])


@callback_router.get("/file/getLastUpdateId", summary="Получить ID последнего обновления файлов")
def callback_file_get_last_update_id(session: Session = Depends(get_db)) -> UpdateIdResponse:
    return UpdateIdResponse(id=get_last_file_update_id(session))


@callback_router.get("/file/getUpdatesByOffset", summary="Получить все обновления, начиная с определенного ID",
                     responses={422: {"model": ExceptionResponse, "description": "Invalid offset"}})
def callback_file_get_updates_by_offset(offset: int, session: Session = Depends(get_db)) -> FileUpdatesResponse:
    if offset < 0:
        raise InvalidParameterException("offset")

    updates_models = get_file_updates_by_offset(session, offset)
    updates_schemes = [convert_model_to_dto_file_update(update) for update in updates_models]
    return FileUpdatesResponse(updates=updates_schemes)


@callback_router.get("/schedule/getLastUpdateId", summary="Получить ID последнего обновления расписания")
def callback_schedule_get_last_update_id(session: Session = Depends(get_db)) -> UpdateIdResponse:
    return UpdateIdResponse(id=get_last_schedule_update_id(session))


@callback_router.get("/schedule/getUpdatesByOffset", summary="Получить все обновления расписания, "
                                                             "начиная с определенного ID")
def callback_schedule_get_updates_by_offset(offset: int, session: Session = Depends(get_db)):
    if offset < 0:
        raise InvalidParameterException("offset")

    updates_models = get_schedule_updates_by_offset(session, offset)
    updates_schemes = [convert_model_to_dto_schedule_update(update) for update in updates_models]
    return ScheduleUpdatesResponse(updates=updates_schemes)
