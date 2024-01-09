# models.py
from extensions import db

# Определение модели книги
class Book(db.Model):
    __tablename__ = 'book'  # Имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор книги
    title = db.Column(db.String(80), nullable=False)  # Название книги
    author = db.Column(db.String(80), nullable=False)  # Автор книги
    description = db.Column(db.String(200))  # Описание книги
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))  # Внешний ключ для жанра
    genre = db.relationship('Genre')  # Связь с таблицей жанров

# Определение модели жанра
class Genre(db.Model):
    __tablename__ = 'genre'  # Имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор жанра
    name = db.Column(db.String(50), nullable=False)  # Название жанра