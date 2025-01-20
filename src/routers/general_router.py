from random import random

from fastapi import APIRouter

from src.routers.file_router import file_controller
from src.routers.schedule_router import schedule_controller
from src.schemes.folder_link_response import FolderLinkResponse
from src.schemes.group_names_response import GroupNamesResponse
from src.schemes.ping_response import PingResponse

general_router = APIRouter(prefix="/general", tags=["general"])


@general_router.get("/ping", summary="Проверка доступности сервера", response_model=PingResponse)
def general_ping():
    return PingResponse(random=random())


@general_router.get("/getGroupNames", summary="Получить список имён групп", response_model=GroupNamesResponse)
def general_get_group_names():
    any_file = file_controller.get_actual_files()[0]
    schedule_file = schedule_controller.get_schedule_day(any_file)
    group_names = sorted(list({group.name for group in schedule_file.groups}))
    return GroupNamesResponse(group_names=group_names)


@general_router.get("/getFolderLink", summary="Получить ссылку на гугл папку", response_model=FolderLinkResponse)
def general_get_folder_link():
    folder_id = file_controller.folder_id
    folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
    return FolderLinkResponse(folder_link=folder_link)
