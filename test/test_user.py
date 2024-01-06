from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi import HTTPException, status
from app.schemas import UserOut
    

def test_login_user(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    assert res.status_code == 200    

@pytest.mark.parametrize('email, password, status_code', (['fistemail@gmail.com', 'passwd@gmail.com', 403],
                                                        [None, None, 422],
                                                        [None, 'password', 422],
                                                        ['email@gmail.com', None, 422]
                                                        ))
def test_login_with_wrong_password(client, test_user, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
    # assert res.json()['details'] == 'Invalid Credentials'


def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json()['message'] == 'hello world'
    
def test_create_user(client):
    res = client.post('/user', json={'email': 'test@example.com', 'password': '123456'})
    UserOut(**res.json())
    assert res.status_code == 201

