class Car():
	def __init__(self, brand: str, model: str, year: int, price: float, status: str):
		self.brand = brand
		self.model = model
		self.year = year
		self.price = price
		self.status = status

	def __repr__(self):
		return f"Car(brand={self.brand}, model={self.model}, year={self.year}, price={self.price}, status={self.status})"
