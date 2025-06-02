from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base
from app.db.base import Base

class CollectorDB(Base):
	__tablename__ = "collectors"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	email = Column(String, unique=True, index=True)
	cars = relationship("CarDB", back_populates="collector", cascade="all, delete-orphan")

class CollectorRepository():
	def __init__(self, db_session):
		self.__db_session = db_session

	def get(self, username: str):
		return self.__db_session.query(CollectorDB).filter(CollectorDB.username == username).options(joinedload(CollectorDB.cars)).first()
	
	def get_by_email(self, email: str):
		return self.__db_session.query(CollectorDB).filter(CollectorDB.email == email).first()
	
	def get_all(self):
		return self.__db_session.query(CollectorDB).options(joinedload(CollectorDB.cars)).all()

	def create(self, collector):
		new_collector = CollectorDB(
			username=collector.username,
			email=collector.email
		)
		self.__db_session.add(new_collector)
		self.__db_session.commit()
		self.__db_session.refresh(new_collector)
		return new_collector
	
	def update_email(self, username: str, update):
		collector = self.get(username)
		print(update)
		print(update.email)
		collector.email = update.email
		self.__db_session.commit()
		self.__db_session.refresh(collector)
		