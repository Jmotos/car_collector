from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

DATABASE_URL = "sqlite:///./car_collector.db"

class Database:
	def __init__(self):
		self.__engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
		from app.car.repository import CarDB
		from app.collector.repository import CollectorDB
		from app.make.repository import MakeDB
		from app.model.repository import ModelDB
		Base.metadata.create_all(self.__engine)

	def get_session(self):
		SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
		return SessionLocal()
