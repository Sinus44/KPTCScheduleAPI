from sqlalchemy.orm import Session

from src.models.file_update_model import FileUpdateModel
from src.models.schedule_update_model import ScheduleUpdateModel


def create_record(session: Session, record):
    try:
        session.add(record)
        session.commit()
        session.refresh(record)
    except Exception as e:
        print(e)

    return record


def create_file_update(session: Session, file_update: FileUpdateModel) -> FileUpdateModel:
    return create_record(session, file_update)


def create_schedule_update(session: Session, schedule_update: ScheduleUpdateModel):
    return create_record(session, schedule_update)


def get_last_file_update(session: Session) -> None | FileUpdateModel:
    return session.query(FileUpdateModel).order_by(FileUpdateModel.id.desc()).first()


def get_last_file_update_id(session: Session) -> int:
    file_update: FileUpdateModel | None = get_last_file_update(session)

    if file_update is None:
        return 0

    else:
        return file_update.id


def get_file_updates_by_offset(session: Session, offset: int) -> list:
    return session.query(FileUpdateModel).filter(FileUpdateModel.id > offset).all()


def get_last_schedule_update(session: Session) -> None | ScheduleUpdateModel:
    return session.query(ScheduleUpdateModel).order_by(ScheduleUpdateModel.id.desc()).first()


def get_last_schedule_update_id(session: Session) -> int:
    schedule_update: ScheduleUpdateModel | None = get_last_schedule_update(session)

    if schedule_update is None:
        return 0

    else:
        return schedule_update.id


def get_schedule_updates_by_offset(session: Session, offset: int) -> list:
    return session.query(ScheduleUpdateModel).filter(ScheduleUpdateModel.id > offset).all()
