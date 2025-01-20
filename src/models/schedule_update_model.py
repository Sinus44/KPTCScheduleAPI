from sqlalchemy import Column, Integer, String, BigInteger

from src.database import Base


class ScheduleUpdateModel(Base):
    __tablename__ = 'schedule_update'

    id = Column(Integer, primary_key=True, index=True)
    update_file_id = Column(String)
    update_time = Column(BigInteger)
    update_group = Column(String)
