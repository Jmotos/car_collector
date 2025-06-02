from fastapi import APIRouter, HTTPException

from .repository import MakeRepository
from ..db.db import Database

router = APIRouter(prefix="/makes")

def get_session():
	db = Database()
	return db.get_session()

@router.get("/")
def get_all():
	session = get_session()
	repository = MakeRepository(session)
	makes = repository.get_all()
	session.close()
	return makes

@router.get("/{name}")
def get_by_name(name: str):
	session = get_session()
	repository = MakeRepository(session)
	make = repository.get(name)
	session.close()
	if not make:
		raise HTTPException(status_code=404, detail="Make not found")
	return make