# from app.car.car import Car
from app.collector.collector import Collector
from app.collector.repository import CollectorRepository, CollectorDB
from app.car.repository import CarRepository

def build_collector(username, session):
	collectorDB = session.query(CollectorDB).filter(CollectorDB.username == username).first()
	if not collectorDB:
		return None
	repository = CollectorRepository(session)
	car_repository = CarRepository(session)
	collector = Collector(collectorDB, repository, car_repository)
	return collector