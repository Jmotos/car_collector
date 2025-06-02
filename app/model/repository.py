from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from ..db.db import Base

class ModelDB(Base):
	__tablename__ = "models"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	make_id = Column(Integer, ForeignKey("makes.id"), nullable=False)
	make = relationship("MakeDB", back_populates="models")

class ModelRepository():
	def __init__(self, db_session):
		self.__db_session = db_session

	def get(self, model_id: int):
		return self.__db_session.query(ModelDB).filter(ModelDB.id == model_id).first()

	def get_from_make(self, make_name: str, model_name: str):
		return self.__db_session.query(ModelDB).filter(
			ModelDB.make.has(name=make_name),
			ModelDB.name == model_name
		).first()
