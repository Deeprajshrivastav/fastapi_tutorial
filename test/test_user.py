from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi import HTTPException, status
from app.schemas import UserOut
from .database import client, session


def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json()['message'] == 'hello world'
    
def test_create_user(client):
    res = client.post('/user', json={'email': 'test@example.com', 'password': '123456'})
    UserOut(**res.json())
    assert res.status_code == 201
    print(res.json())

def test_create1_user(client):
    res = client.post('/user', json={'email': 'test@example.com', 'password': '123456'})
    UserOut(**res.json())
    assert res.status_code == 201
    print(res.json())
