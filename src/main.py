import logging
import logging.config
import logging.handlers
import threading

import colorama
import uvicorn
from fastapi import FastAPI

from src.config import API_CONFIG
from src.database import Base, engine
from src.routers.bells_router import bells_router
from src.routers.callback_router import file_update_controller, callback_router
from src.routers.file_router import file_router
from src.routers.general_router import general_router
from src.routers.schedule_router import schedule_router

colorama.just_fix_windows_console()

Base.metadata.create_all(bind=engine)

api = FastAPI(
    title="KPTC Schedule API",
    description="API for getting schedule",
    version="1.1",
    root_path="."
)

api.include_router(general_router)
api.include_router(bells_router)
api.include_router(file_router)
api.include_router(schedule_router)
api.include_router(callback_router)


def main():
    logging.config.fileConfig("./src/log_config.ini")
    threading.Thread(target=file_update_controller.start, daemon=True).start()
    uvicorn.run("src.main:api", host=API_CONFIG["host"], port=API_CONFIG["port"], workers=1,
                log_config="./src/log_config.ini")


if __name__ == "__main__":
    main()
