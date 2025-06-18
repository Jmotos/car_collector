from fastapi import APIRouter, HTTPException
from typing import List

from .repository import CollectorRepository
from .collector import Collector
from .model import CollectorModel, CollectorUpdateModel, CollectorOutputModel
from ..car.model import CarModel, CarOutputModel
from ..db.db import Database
import builder

router = APIRouter(prefix="/collectors")

def get_session():
	db = Database()
	return db.get_session()

def get_output_collector(collector):
	return CollectorOutputModel(
		# id=collector.id,
		username=collector.username,
		email=collector.email,
		cars=[get_output_car(car) for car in collector.cars])

def get_output_collectors(collectors):
	return [CollectorOutputModel(
		username=collector.username,
		email=collector.email,
		cars=[get_output_car(car) for car in collector.cars]
	) for collector in collectors]

def get_output_car(car):
	return CarOutputModel(
		make=car.make,
		model=car.model,
		year=car.year,
		price=car.price
	)

@router.get("/", response_model=List[CollectorOutputModel])
def get_all():
	session = get_session()
	repository = CollectorRepository(session)
	collectors = repository.get_all()
	session.close()
	return [get_output_collector(collector) for collector in collectors]

@router.get("/{username}", response_model=CollectorOutputModel)
def get_by_username(username: str):
	session = get_session()
	repository = CollectorRepository(session)
	collector = repository.get(username)
	session.close()
	if not collector:
		raise HTTPException(status_code=404, detail="Collector not found")
	return get_output_collector(collector)

@router.post("/")
def create(model: CollectorModel):
	session = get_session()
	repository = CollectorRepository(session)
	collector = Collector(model, repository)
	collector.persist()
	session.close()
	return {
		"msg": "Collector created successfully",
		"status_code": 201,
		"collector": get_output_collector(collector)
	}

@router.delete("/{username}")
def delete(username: str):
	session = get_session()
	repository = CollectorRepository(session)
	collectorExists = repository.delete(username)
	session.close()
	if not collectorExists:
		raise HTTPException(status_code=404, detail="Collector not found")
	return {
		"msg": "Collector deleted successfully",
		"status_code": 200
	}

@router.put("/{username}")
def update_email(username: str, update: CollectorUpdateModel):
	session = get_session()
	repository = CollectorRepository(session)
	collector = repository.get(username)
	if not collector:
		session.close()
		raise HTTPException(status_code=404, detail="Collector not found")
	if not update.email:
		session.close()
		raise HTTPException(status_code=400, detail="Email is required for update")
	repository.update_email(username, update)
	session.close()
	return {
		"msg": "Collector updated successfully",
		"status_code": 200,
		"collector": get_output_collector(collector)
	}

@router.get("/{username}/cars", response_model=List[CarOutputModel])
def get_cars(username: str):
	session = get_session()
	collector = builder.build_collector(username, session)
	session.close()
	if not collector:
		raise HTTPException(status_code=404, detail="Collector not found")
	return [get_output_car(car) for car in collector.cars]

@router.post("/{username}/car")
def add_car(username: str, car: CarModel):
	session = get_session()
	collector = builder.build_collector(username, session)
	if not collector:
		session.close()
		raise HTTPException(status_code=404, detail="Collector not found")
	collector.add_car(car)
	session.close()
	return {
		"msg": f"Car added successfully to {username}",
		"status_code": 201,
		"car": get_output_car(car)
	}