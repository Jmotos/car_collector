from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

class CarModel(BaseModel):
	brand: str = Field(..., min_length=1, max_length=20, description="Brand of the car")
	model: str = Field(..., min_length=1, max_length=50, description="Model of the car")
	year: Optional[int] = Field(None, ge=0, description="Year must be a non-negative integer")
	price: Optional[int] = Field(None, ge=0, description="Price must be a non-negative integer")

	@field_validator("brand")
	def validate_brand(cls, value):
		# TODO
		# check if the brand exists in the database
		return value
	
	@model_validator(mode="after")
	def model_exists(cls, car):
		# TODO
		# check if the car brand-model exists in the database
		return car