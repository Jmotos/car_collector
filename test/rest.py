import requests

def post(url, data):
	response = requests.post(url, json=data)
	print(f"Código de respuesta: {response.status_code}")
	print(f"Respuesta: {response.json()}")

def get(url):
	response = requests.get(url)
	print(f"Código de respuesta: {response.status_code}")
	print(f"Respuesta: {response.json()}")

collectors_host = "http://127.0.0.1:8000/collectors/"
makes_host = "http://127.0.0.1:8000/makes/"
collector_username = "Juanito"
new_collector = {
    "username": collector_username,
    "email": "juan@example.com"
}
new_car = {
	"make": "Toyota",
	"model": "Corolla",
	"year": 2020,
	"price": 20000
}

print("Create a new collector and add a car")
post(collectors_host, new_collector)
post(f"{collectors_host}/{collector_username}/cars", new_car)

print("Update collector's email")
update_data = { "email": "foo@gmail.com" }
post(f"{collectors_host}/{collector_username}", update_data)

print("Get a specific collector information")
get(f"{collectors_host}/{collector_username}")

print("Get all collectors information")
get(collectors_host)

print("Get all car makes")
get(makes_host)
