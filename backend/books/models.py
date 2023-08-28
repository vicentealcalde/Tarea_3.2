from books.db import db
import sqlalchemy as sa

class Author(db.Model):
    name = db.Column(db.String, nullable=False)
    openlibrary_key = db.Column(db.String, nullable=False)
    books = sa.orm.relationship("Book", back_populates="author")

class Book(db.Model):
    title = db.Column(db.String, nullable=False)
    openlibrary_key = db.Column(db.String, nullable=False)
    author_id = db.Column(sa.ForeignKey('author.id'))
    author = sa.orm.relationship("Author", back_populates="books")
    description = db.Column(db.String)
    ratings = sa.orm.relationship("Rating", back_populates="book")

class Rating(db.Model):
    book_id = db.Column(sa.ForeignKey('book.id'))
    book = sa.orm.relationship("Book", back_populates="ratings")
    score = db.Column(db.Integer)
    

