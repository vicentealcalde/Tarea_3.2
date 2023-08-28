from flask import Flask, make_response
from flask import render_template, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_alembic import Alembic
from .db import db
from books.models import Author, Book, Rating
from itertools import chain
import csv
from alembic import op
import os 

cont = 0

def create_app():
    # create and configure the app
    app = Flask(__name__)
    
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db/postgres"
    alembic = Alembic()

    db.init_app(app)
    alembic.init_app(app)

    import books.models

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # a simple page that says hello
    @app.route('/')
    def base():
        return render_template('index.html')

    @app.route('/authors')
    def authors_index():
        authors = db.session.execute(db.select(Author)).scalars()
        authors_dicts = []
        for author in authors:
            ratings = list(chain(*list(map(lambda x: x.ratings, author.books))))
            print(ratings)
            authors_dicts.append({
                'item': author,
                'average_score': 0 if len(ratings) == 0 else sum(map(lambda x: x.score, ratings)) / len(ratings)
            })
        return render_template('authors.html', authors=authors_dicts)
    
    @app.route('/books')
    def books_index():
        books = db.session.execute(db.select(Book)).scalars()
        books_dicts = []
        for book in books:
            books_dicts.append({
                'item': book,
                'average_score': 0 if len(book.ratings) == 0 else sum(map(lambda x: x.score, book.ratings))/len(book.ratings)
            })
        return render_template('books.html', books=books_dicts)
    
    @app.route('/populate')
    def populate_db():
        script_directory = os.path.dirname(__file__)
        db_file_folder = os.path.join(script_directory, 'database_files')
        authors_csv_path = os.path.join(db_file_folder, 'authors.csv')
        books_csv_path = os.path.join(db_file_folder, 'books.csv')
        ratings_csv_path = os.path.join(db_file_folder, 'ratings.csv')
        
        with app.app_context():
            try:
                with open(authors_csv_path, 'r') as authors_file:
                    authors_reader = csv.DictReader(authors_file, delimiter=';')
                    for row in authors_reader:
                        try:
                            author = Author(name=row['name'], openlibrary_key=row['key'])
                            db.session.add(author)
                            
                        except Exception as e:
                            print("Wrong key for row: ", row)
                            
                db.session.commit()
                
                with open(books_csv_path, 'r') as books_file:
                    books_reader = csv.DictReader(books_file, delimiter=';')
                    for row in books_reader:
                        
                        try:
                            author_id = row['author']
                            if author_id.startswith('/authors/'):
                                author = Author.query.filter_by(openlibrary_key=author_id).first()
                                if author:
                                    author_id = author.id
                                else:
                                    print(f"author not found for key: {author_id}", flush=True)
                                    continue
                            
                            book = Book(title=row['title'], openlibrary_key=row['key'], author_id=author_id, description=row['description'])
                            db.session.add(book)
                            
                        except Exception as e:
                            print("Wrong key for row: ", row)
                            
                db.session.commit()
                
                with open(ratings_csv_path, 'r') as ratings_file:
                    ratings_reader = csv.DictReader(ratings_file, delimiter=';')
                    for row in ratings_reader:
                        book = Book.query.filter_by(openlibrary_key=row['work']).first()
                        rating = Rating(book_id=book.id, score=row['score'])
                        db.session.add(rating)
                        
                db.session.commit()
                
            except Exception as e:
                print("An error occurred while populating the database: ", e)
                
        response = "data cargada"

    # if not os.path.exists('database_initialized.txt'):
    #     populate_db()
    #     with open('database_initialized.txt', 'w') as f:
    #         f.write('initialized')

            
    return app

    
