from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic models for data validation
class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text_review: str
    rating: int

# In-memory storage for demonstration purposes
books_db = []
reviews_db = []

# Endpoints
@app.post("/books/")
async def add_book(book: Book):
    books_db.append(book)
    return JSONResponse(content=jsonable_encoder(book), status_code=201)

@app.post("/books/{book_id}/reviews/")
async def submit_review(book_id: int, review: Review):
    try:
        book = books_db[book_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews_db.append({"book_id": book_id, **review.dict()})
    
    return JSONResponse(content=jsonable_encoder(review), status_code=201)

@app.get("/books/")
async def retrieve_books(author: str = None, publication_year: int = None):
    filtered_books = [book for book in books_db if (
        (author is None or book.author == author) and
        (publication_year is None or book.publication_year == publication_year)
    )]
    return filtered_books

@app.get("/books/{book_id}/reviews/")
async def retrieve_reviews(book_id: int):
    try:
        reviews = [review for review in reviews_db if review["book_id"] == book_id]
        return reviews
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")
    

# main.py continued...

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
engine = create_engine("sqlite:///./test.db")

# Database models
class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    publication_year = Column(Integer)

class ReviewDB(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text_review = Column(String)
    rating = Column(Integer)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Update endpoints to use the database

# Example: Update /books/ endpoint
@app.post("/books/")
async def add_book(book: Book, db: Session = Depends(get_db)):
    db_book = BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return JSONResponse(content=jsonable_encoder(book), status_code=201)


# main.py continued...

import asyncio

# Advanced Feature: Background Task
async def send_confirmation_email(book_id: int, text_review: str):
    # Simulated background task (replace with actual email sending logic)
    await asyncio.sleep(5)
    print(f"Email sent for review on book {book_id}: {text_review}")

# Example: Update /books/{book_id}/reviews/ endpoint
@app.post("/books/{book_id}/reviews/")
async def submit_review(book_id: int, review: Review, db: Session = Depends(get_db)):
    try:
        book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        review_db = ReviewDB(**review.dict(), book_id=book_id)
        db.add(review_db)
        db.commit()

        # Trigger background task
        asyncio.create_task(send_confirmation_email(book_id, review.text_review))

        return JSONResponse(content=jsonable_encoder(review), status_code=201)
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")



