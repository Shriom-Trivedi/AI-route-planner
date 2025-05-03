import requests

data = {"user_intent": "intent", "email": "john@wick.com"}

response = requests.post("http://localhost:8000/calculate_route", json=data)

print("Status code:", response.status_code)
print("Raw text response:", response.text)