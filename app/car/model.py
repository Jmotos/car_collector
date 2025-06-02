from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from app.make.repository import MakeRepository
from app.model.repository import ModelRepository
from app.db.db import Database

database = Database()

def make_exists(make: str):
	session = database.get_session()
	repository = MakeRepository(session)
	existing_make = repository.get(make)
	session.close()
	return existing_make is not None

def model_exists_for_make(make: str, model: str):
	session = database.get_session()
	repository = ModelRepository(session)
	existing_model = repository.get_from_make(make, model)
	session.close()
	return existing_model is not None

class CarModel(BaseModel):
	make: str = Field(..., min_length=1, max_length=20, description="Make of the car")
	model: str = Field(..., min_length=1, max_length=50, description="Model of the car")
	year: Optional[int] = Field(None, ge=0, description="Year must be a non-negative integer")
	price: Optional[int] = Field(None, ge=0, description="Price must be a non-negative integer")

	@field_validator("make")
	def validate_make(cls, value):
		if not make_exists(value):
			raise ValueError(f"Make '{value}' does not exist.")
		return value

	@model_validator(mode="after")
	def model_exists(cls, car):
		if not model_exists_for_make(car.make, car.model):
			raise ValueError(f"Model '{car.model}' for make '{car.make}' does not exist.")
		return car

class CarOutputModel(BaseModel):
	make: str
	model: str
	year: int
	price: int