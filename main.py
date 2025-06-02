import logging
import os
import asyncio
import httpx

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.car.model import CarModel
from app.collector.api import router as collector_router
from app.make.api import router as make_router
from app.make.repository import MakeRepository
from app.db.db import Database

app = FastAPI(
	title="Car collector API",
	description="An API for managing car collections.",
    version="1.0.0"
)

database = Database()

async def initialize_makes_and_models(session):
	makes_repository = MakeRepository(session)
	if not makes_repository.is_empty():
		session.close()
		return
	load_dotenv()
	makes_url = "https://car-api2.p.rapidapi.com/api/models?sort=id&direction=asc&year=2020&verbose=yes"
	headers = {
		"x-rapidapi-host": "car-api2.p.rapidapi.com",
		"x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
	}
	async with httpx.AsyncClient() as client:
		response = await client.get(makes_url, headers=headers)
		json_response = response.json()
	makes_repository.create_makes_and_models(json_response["data"])
	session.close()

app.include_router(collector_router)
app.include_router(make_router)

@app.on_event("startup")
async def startup_event():
    session = database.get_session()
    await initialize_makes_and_models(session)
