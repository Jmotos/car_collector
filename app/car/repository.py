from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from ..db.db import Base

class CarDB(Base):
	__tablename__ = "cars"
	id = Column(Integer, primary_key=True, index=True)
	brand = Column(String, index=True)
	model = Column(String, index=True)
	year = Column(Integer)
	price = Column(Integer)
	collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
	collector = relationship("CollectorDB", back_populates="cars")

class CarRepository():
	def __init__(self, db_session):
		self.__db_session = db_session

	def add_car(self, username: str, car):
		new_car = CarDB(
			brand=car.brand,
			model=car.model,
			year=car.year,
			price=car.price
		)
		self.__db_session.add(new_car)
		self.__db_session.commit()
		self.__db_session.refresh(new_car)
		return new_car
