import os
from flask import Flask, jsonify
from models import db
from flask_migrate import Migrate
from routes import books_bp
from db_repository import BooksRepository
import traceback
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('api.log')
app.logger.addHandler(handler)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(books_bp, url_prefix='/books')

@app.route('/')
def home():
    return jsonify(message="Books API")


@app.route('/health')
def health_check():
    return jsonify(status="ok")


@app.errorhandler(Exception)
def global_exception_handler(e):
    traceback.print_exc()
    app.logger.critical(f"Unexpected error: {str(e)}", e)
    BooksRepository(db.session).rollback()
    return jsonify(message="Unexpected server error", steck=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
