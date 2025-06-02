import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.car.model import CarModel
from app.car.api import router as car_router
from app.collector.api import router as collector_router

logging.basicConfig(
	level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
	title="Car collector API",
	description="An API for managing car collections.",
    version="1.0.0"
)

app.include_router(car_router)
app.include_router(collector_router)

@app.middleware("http")
def log_requests(request, call_next):
	logger.info(f"Request: {request.method} {request.url}")
	response = call_next(request)
	logger.info(f"Response status: {response}")
	return response

@app.get("/offers")
def get_offers():
	return {"msg": "Hola mundo!!!"}

@app.get("/offers/{brand}")
def get_offers_by_brand():
	return {"msg": "Hola mundo!!!"}

@app.get("/offers/{brand}/{model}")
def get_offers_by_model():
	return {"msg": "Hola mundo!!!"}

@app.post("/offers")
def make_offer(username: str, car: CarModel):
	return {"msg": "Hola mundo!!!"}


STATUS = ["owner", "available", "sold"]