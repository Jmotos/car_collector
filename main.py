import os
import httpx
import logging
import json

from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

from app.collector.api import router as collector_router
from app.make.api import router as make_router
from app.make.repository import MakeRepository
from app.db.db import Database

app = FastAPI(
	title="Car collector API",
	description="An API for managing car collections.",
    version="1.0.0"
)

logging.basicConfig(
	level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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

async def log_request_body(request):
	body = await request.body()
	if body:
		body_data = json.loads(body)
		logger.info(f"Request: {request.method} {request.url} Body: {body_data}")
	else:
		logger.info(f"Request: {request.method} {request.url} Body: <empty>")
	async def receive():
		return {"type": "http.request", "body": body}
	return receive

async def log_response(response):
	response_body = b""
	async for chunk in response.body_iterator:
		response_body += chunk
	try:
		body_data = json.loads(response_body)
		logger.info(f"Response {response.status_code}: {body_data}")
	except Exception:
		logger.info(f"Response {response.status_code}: {response_body.decode('utf-8', errors='replace')}")
	return response_body

@app.middleware("http")
async def log_requests(request, call_next):
	receive = await log_request_body(request)
	response = await call_next(Request(request.scope, receive))
	response_body = await log_response(response)
	return Response(
		content=response_body,
		status_code=response.status_code,
		headers=dict(response.headers),
		media_type=response.media_type
	)