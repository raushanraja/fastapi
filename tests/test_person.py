from http import client
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)



def test_read_user():
    response = client.get('/')
    assert response.status_code == 200
    print(response.json())