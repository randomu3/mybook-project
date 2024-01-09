# app.py
from flask import render_template, request, redirect, url_for
from extensions import app, db
from models import Book, Genre

# Маршрут для добавления книги
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Получаем все жанры из базы данных
    genres = Genre.query.all()
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        genre_name = request.form.get('genre')
        new_genre_name = request.form.get('new_genre')

        # Если введен новый жанр, проверяем его наличие в базе или создаем новый
        if new_genre_name:
            genre = Genre.query.filter_by(name=new_genre_name).first()
            if not genre:
                genre = Genre(name=new_genre_name)
                db.session.add(genre)
        else:
            # Иначе используем выбранный жанр
            genre = Genre.query.filter_by(name=genre_name).first()

        # Создаем новую книгу и добавляем ее в базу данных
        new_book = Book(title=title, author=author, description=description)
        new_book.genre = genre
        db.session.add(new_book)
        db.session.commit()
        # После добавления книги перенаправляем пользователя на список книг
        return redirect(url_for('book_list'))

    # Отображаем страницу добавления книги
    return render_template('add_book.html', genres=genres)

# Маршрут для отображения списка книг
@app.route('/books')
def book_list():
    # Получаем все книги из базы данных
    books = Book.query.all()
    # Отображаем страницу со списком книг
    return render_template('book_list.html', books=books)

# Маршрут для поиска книг
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        # Фильтруем книги по названию или автору
        books = Book.query.filter((Book.title.contains(search_term)) | (Book.author.contains(search_term))).all()
        # Отображаем страницу со списком найденных книг
        return render_template('book_list.html', books=books)
    # Отображаем страницу поиска
    return render_template('search.html')

# Маршрут для отображения деталей книги
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    # Получаем книгу по ID или возвращаем ошибку 404
    book = Book.query.get_or_404(book_id)
    # Отображаем страницу с деталями книги
    return render_template('book_detail.html', book=book)

# Маршрут для удаления книги
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    # Получаем книгу по ID или возвращаем ошибку 404
    book_to_delete = Book.query.get_or_404(book_id)
    # Удаляем книгу из базы данных
    db.session.delete(book_to_delete)
    db.session.commit()
    # Перенаправляем пользователя на список книг
    return redirect(url_for('book_list'))

# Маршрут для главной страницы
@app.route('/')
def index():
    # Получаем все книги из базы данных
    books = Book.query.all()
    # Отображаем главную страницу
    return render_template('index.html', books=books)

# Точка входа в приложение
if __name__ == '__main__':
    # Создаем таблицы в базе данных, если их нет
    with app.app_context():
        db.create_all()
    # Запускаем приложение
    app.run(debug=True)