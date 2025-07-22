from pydantic import BaseModel, field_validator
from typing import Optional
from pydantic import ValidationError

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    rating: Optional[float]
    price: float

    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_orm_list(books):
        result = []
        for book in books:
            result.append(BookSchema.from_orm(book).model_dump())
        return result

    @field_validator('title', mode='before')
    @classmethod
    def validate_title(cls, value):
        if len(value) > 120:
            raise ValueError("Title is too long")
        return value

    @field_validator('author', mode='before')
    @classmethod
    def validate_author(cls, value):
        if len(value) > 120:
            raise ValueError("author is too long")
        return value

    @field_validator('pages', mode='before')
    @classmethod
    def validate_pages(cls, value):
        if value < 0:
            raise ValueError("Value for pages cannot be less than 0")
        return value

    @field_validator('id', mode='before')
    @classmethod
    def validate_pages(cls, value):
        if value < 0:
            raise ValueError("Value for id cannot be less than 0")
        return value

    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Value for price cannot be less than 0")
        return value

    @field_validator('rating', mode='before')
    @classmethod
    def validate_rating(cls, value):
        if value < 0:
            raise ValueError("Value for rating cannot be less than 0")
        return value

    @staticmethod
    def custom_validate_price_and_rating(price, rating):
        if price and price < 0:
            raise ValueError("Value for price cannot be less than 0")
        if rating and rating < 0:
            raise ValueError("Value for rating cannot be less than 0")
