from sqlalchemy import Column, Integer, String, SmallInteger, BigInteger

from src.database import Base


class FileUpdateModel(Base):
    __tablename__ = 'file_update'

    id = Column(Integer, primary_key=True, index=True)
    update_file_id = Column(String)
    update_time = Column(BigInteger)
    update_type = Column(SmallInteger)
