from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi import HTTPException, status
from app.schemas import UserOut
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {'email': 'test1@example.com', 'password': '123456'}
    res = client.post('/user', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
    

def test_login_user(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    assert res.status_code == 200    

def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json()['message'] == 'hello world'
    
def test_create_user(client):
    res = client.post('/user', json={'email': 'test@example.com', 'password': '123456'})
    UserOut(**res.json())
    assert res.status_code == 201

