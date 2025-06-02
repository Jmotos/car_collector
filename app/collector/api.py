from fastapi import APIRouter, HTTPException

from .repository import CollectorRepository
from .collector import Collector
from .model import CollectorModel, CollectorUpdateModel
from ..car.model import CarModel
from ..db.db import Database
import builder
from ..logger.logger import logger

router = APIRouter(prefix="/collectors")

def get_session():
	db = Database()
	return db.get_session()


@router.middleware("http")
def log_requests(request, call_next):
	logger.info(f"Request: {request.method} {request.url}")
	response = call_next(request)
	logger.info(f"Response status: {response}")
	return response

@router.get("/")
def get_all():
	session = get_session()
	repository = CollectorRepository(session)
	collectors = repository.get_all()
	session.close()
	return collectors

@router.get("/{username}")
def get_by_username(username: str):
	# logger.info(f"Username: {username}")
	session = get_session()
	repository = CollectorRepository(session)
	collector = repository.get(username)
	session.close()
	if not collector:
		raise HTTPException(status_code=404, detail="Collector not found")
	return collector

@router.post("/")
def create(model: CollectorModel):
	session = get_session()
	repository = CollectorRepository(session)
	collector = Collector(model, repository)
	collector.persist()
	session.close()
	return {"msg": "Collector created successfully", "collector": collector}

@router.put("/{username}")
def update_email(username: str, update: CollectorUpdateModel):
	session = get_session()
	repository = CollectorRepository(session)
	collector = repository.get(username)
	if not collector:
		session.close()
		raise HTTPException(status_code=404, detail="Collector not found")
	repository.update_email(username, update)
	session.close()
	return {"msg": "Collector updated successfully", "collector": collector}

@router.get("/{username}/cars")
def get_cars(username: str):
	session = get_session()
	collector = builder.build_collector(username, session)
	session.close()
	if not collector:
		raise HTTPException(status_code=404, detail="Collector not found")	
	cars = collector.cars
	return {"msg": cars}

@router.post("/{username}/car")
def add_car(username: str, car: CarModel):
	session = get_session()
	collector = builder.build_collector(username, session)
	collector.add_car(car)
	session.close()
	return {"msg": "Car added successfully", "car": car}