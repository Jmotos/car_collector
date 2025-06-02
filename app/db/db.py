from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./car_collector.db"
Base = declarative_base()

class Database:
	def __init__(self):
		self.__engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
		# Crear todas las tablas si no existen
		from app.car.repository import CarDB
		from app.collector.repository import CollectorDB
		Base.metadata.create_all(self.__engine)

	def get_session(self):
		SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
		return SessionLocal()
