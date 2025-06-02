class Collector():
	def __init__(self, data, repository, cars_repository=None):
		self.__repository = repository
		self.__cars_repository = cars_repository
		self.__id = data.id if data.id else None
		self.__username = data.username
		self.__email = data.email
		collector_db = self.__repository.get(self.__username)
		self.cars = collector_db.cars if collector_db else []
		self.offers = []
	
	@property
	def email(self):
		return self.__email

	@email.setter
	def email(self, email):
		self.__email = email
		self.__repository.update_email(self.__username, email)

	@property
	def username(self):
		return self.__username

	def add_car(self, car):
		self.__cars_repository.add_car(self.__id, car)

	def persist(self):
		collector = self.__repository.create(self)
		self.__id = collector.id
	