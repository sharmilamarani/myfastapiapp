from fastapi.testclient import TestClient
from fastapi_app import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

# Database setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Override the database dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test cases
def test_add_book():
    response = client.post("/books/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2022})
    assert response.status_code == 201
    assert response.json() == {"title": "Test Book", "author": "Test Author", "publication_year": 2022}

def test_add_duplicate_book():
    # Adding the same book again should return 201 as well, assuming book titles can be duplicated
    response = client.post("/books/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2022})
    assert response.status_code == 201

def test_add_invalid_book():
    # Trying to add a book with missing required fields should return a 422 Unprocessable Entity
    response = client.post("/books/", json={"author": "Test Author", "publication_year": 2022})
    assert response.status_code == 422

def test_submit_review():
    # Assuming there is a book with id 1 (ensure this based on your actual data or setup)
    response = client.post("/books/1/reviews/", json={"text_review": "Great book!", "rating": 5})
    assert response.status_code == 201
    assert response.json() == {"text_review": "Great book!", "rating": 5}

def test_submit_review_invalid_book():
    # Trying to submit a review for a non-existing book should return a 404 Not Found
    response = client.post("/books/999/reviews/", json={"text_review": "Great book!", "rating": 5})
    assert response.status_code == 404


