from typing import Optional, List

from models import Books
from sqlalchemy.orm import Session


class BooksRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, book_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(id=book_id).one_or_none()

    def get_all(self, title_filter, min_pages_filter) -> List[Books]:
        query_books = Books.query

        if title_filter:
            query_books = query_books.filter(Books.title.ilike(f'%{title_filter}%'))
        if min_pages_filter:
            query_books = query_books.filter(Books.pages >= min_pages_filter)

        return query_books.all()

    def add_book(self, book: Books):
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def update_price_and_rating(self, book_id: int, price, rafting):
        book = self.get_by_id(book_id)

        if price:
            book.price = price
        if rafting:
            book.rating = rafting

        self.session.commit()
        self.session.refresh(book)
        return book

    def rollback(self):
        self.session.rollback()
