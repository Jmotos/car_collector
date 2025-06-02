from fastapi import APIRouter, HTTPException

from .model import CarModel
from ..collector.model import CollectorRepository
from .car import Car
from ..db.db import Database

router = APIRouter(prefix="/my-cars")

def get_session():
	db = Database()
	return db.get_session()

def get_collector(username: str, session):
	repository = CollectorRepository(session)
	collector = repository.get(username)
	if not collector:
		raise HTTPException(status_code=404, detail="User not found")
	return collector

# @router.get("/")
# def get_my_cars_info(username: str):
# 	session = get_session()
# 	collector = get_collector(username, session)
# 	session.close()
# 	return {"msg": collector.cars}

@router.post("/")
def add_car(username: str, car_model: CarModel):
	session = get_session()
	collector = get_collector(username, session)
	car = Car(car_model)
	collector.add_car(car)
	session.close()
	return {"msg": "Car added successfully", "car": car}