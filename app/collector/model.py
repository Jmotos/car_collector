from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional

from .repository import CollectorRepository
from app.car.model import CarOutputModel
from app.db.db import Database

database = Database()

def email_exists(email: str):
	session = database.get_session()
	repository = CollectorRepository(session)
	existing_user = repository.get_by_email(email)
	session.close()
	return existing_user is not None

def username_exists(username: str):
	session = database.get_session()
	repository = CollectorRepository(session)
	existing_user = repository.get(username)
	session.close()
	return existing_user is not None

class CollectorModel(BaseModel):
	id: Optional[int] = None
	username: str = Field(..., min_length=8, max_length=20)
	email: EmailStr

	@field_validator("username")
	def validate_username(cls, value):
		if username_exists(value):
			raise ValueError(f"Username '{value}' already exists.")
		return value

	@field_validator("email")
	def validate_email(cls, value):
		if email_exists(value):
			raise ValueError(f"Email '{value}' already exists.")
		return value

class CollectorUpdateModel(CollectorModel):
	username: Optional[str] = None
	email: Optional[EmailStr] = None

class CollectorOutputModel(BaseModel):
	username: str
	email: EmailStr
	cars: List[CarOutputModel] = []