from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.db.db import Base
from app.model.repository import ModelDB

class MakeDB(Base):
	__tablename__ = "makes"
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True, unique=True)
	models = relationship("ModelDB", back_populates="make", cascade="all, delete-orphan")

class MakeRepository():
	def __init__(self, db_session):
		self.__db_session = db_session

	def is_empty(self):
		return self.__db_session.query(MakeDB).count() == 0

	def get(self, name: str):
		return self.__db_session.query(MakeDB).filter(MakeDB.name == name).first()

	def get_all(self):
		return self.__db_session.query(MakeDB).all()

	def __create_make(self, make_id, make_name):
		make = MakeDB(id=make_id, name=make_name)
		self.__db_session.add(make)
		return make
	
	def __create_model(self, id, name, make):
		model = ModelDB(id=id, name=name, make=make)
		self.__db_session.add(model)

	def create_makes_and_models(self, data):
		makes_dict = {}

		for item in data:
			make_name = item['make']['name']
			model_name = item['name']
			make_id = item['make_id']
			model_id = item['id']

			if make_name in makes_dict:
				make = makes_dict[make_name]
			else:
				make = self.__create_make(make_id, make_name)
				makes_dict[make_name] = make
			self.__create_model(model_id, model_name, make)

		self.__db_session.commit()