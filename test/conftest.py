 from fastapi.testclient import TestClient
from app.main import app
from app import models
import pytest
from sqlalchemy import create_engine
from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker
from app.config import Setting
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.oath2 import create_access_token

setting  = Setting()


SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    return session


@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    
@pytest.fixture(scope='function')
def test_user(client):
    user_data = {'email': 'test1@example.com', 'password': '123456'}
    res = client.post('/user', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(client, test_user):
    token = create_access_token({'user_id': test_user['id']})
    return token

@pytest.fixture
def authorized_client(client, token):
    client.headers['Authorization'] = f"Bearer {token}"
    return client

@pytest.fixture
def create_test_post(test_user, session):
    post_data = []
    print(type(session))
    for i in range(2, 12):
        post = {'title': f'title {i}', 'content': f'content {i}', 'user_id': test_user['id']}
        print(test_user['id'])
        post_data.append(post)
    def create_post(post):
        return models.Post(**post)
    posts = map(create_post, post_data)
    posts = list(posts)
    #print(posts)
    
    session.add_all(posts)
    session.commit()