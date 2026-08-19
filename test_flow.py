import requests

# Get token for tenant 5
print("Getting token for tenant 5...")
resp = requests.post("http://127.0.0.1:8000/token", data={"username": "5", "password": "password"})
print(resp.status_code, resp.text)
token = resp.json()["access_token"]

# Create student
print("Creating student...")
headers = {"Authorization": f"Bearer {token}"}
data = {
    "name": "Test User",
    "age": 20,
    "dept": "CS",
    "mail": "test@test.com"
}
resp2 = requests.post("http://127.0.0.1:8000/students", json=data, headers=headers)
print(resp2.status_code, resp2.text)
