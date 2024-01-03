from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker
from app.config import Setting
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from app.database import get_db, Base


setting  = Setting()


SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)