from flask import Blueprint, jsonify, request, current_app
from models import db, Books
from db_repository import BooksRepository
from DTOs import BookSchema
from pydantic import ValidationError

books_bp = Blueprint('books_bp', __name__)


@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    db_repo = BooksRepository(db.session)
    book = db_repo.get_by_id(book_id)
    if not book:
        return jsonify(message="The book is not found"), 404
    return BookSchema.from_orm(book).model_dump()


@books_bp.route('/', methods=['GET'])
def get_books():
    title_filter = request.args.get('title')
    min_pages_filter = request.args.get('min_pages')
    db_repo = BooksRepository(db.session)
    books = db_repo.get_all(title_filter, min_pages_filter)
    return BookSchema.from_orm_list(books)


@books_bp.route('/', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        new_book = BookSchema(**data)
    except ValidationError as e:
        error_msgs = []
        for err in e.errors():
            error_msgs.append(f"Field: {err['loc']}, error: {err['msg']}")
        msg = '; '.join(error_msgs)
        current_app.logger.warning(f"Bad request for creating a new book. Error: {msg}")
        return jsonify({"error": "Validation failed", "details": msg}), 400

    db_repo = BooksRepository(db.session)
    if db_repo.get_by_id(new_book.id):
        current_app.logger.error(f"Bad request for creating a new book. Book id {new_book.id} already exist")
        return jsonify({"error": "Validation failed", "details": f"Book id {new_book.id} already exist"}), 422

    book = Books(**new_book.model_dump())
    book = db_repo.add_book(book)
    current_app.logger.info(f"Successful added new book: {book.id}, title: {book.title}")
    return BookSchema.from_orm(book).model_dump(), 201


@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    update_data = request.get_json()
    try:
        BookSchema.custom_validate_price_and_rating(update_data.get("price"), update_data.get("rating"))
    except ValueError as err:
        current_app.logger.warning(f"Bad request for updating book {book_id}. Error: {str(err)}")
        return jsonify({"error": "Validation failed", "details": str(err)}), 400

    db_repo = BooksRepository(db.session)
    book = db_repo.update_price_and_rating(book_id, update_data.get("price"), update_data.get("rating"))
    current_app.logger.info(f"Successful updated new book: {book.id}, title: {book.title}")
    return BookSchema.from_orm(book).model_dump()
