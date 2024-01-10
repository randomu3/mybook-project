# test_app.py
import unittest
from app import app, db
from models import Book, Genre

class BookTestCase(unittest.TestCase):
    # Настройка перед каждым тестом
    def setUp(self):
        # Конфигурация тестовой базы данных
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Создание структуры базы данных
        with app.app_context():
            db.create_all()

    # Очистка после каждого теста
    def tearDown(self): 
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Тест фильтрации книг по жанру
    def test_filter_books_by_genre(self):
        with app.app_context():
            genre = Genre(name="Fantasy")
            book1 = Book(title="Fantasy Book 1", author="Author 1", genre=genre)
            book2 = Book(title="Other Book", author="Author 2")
            db.session.add_all([genre, book1, book2])
            db.session.commit()

        response = self.app.get('/books?genre=Fantasy', follow_redirects=True)
        self.assertIn(b'Fantasy Book 1', response.data)
        self.assertNotIn(b'Other Book', response.data)

    # Тест добавления книги
    def test_add_book(self):
        response = self.app.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            genre='Test Genre'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    # Тест обработки невалидных данных при добавлении книги
    def test_add_invalid_book(self):
        response = self.app.post('/add_book', data=dict(
            title='',  # пустое название
            author='Test Author',
            description='Test Description',
            genre='Test Genre'
        ), follow_redirects=True)
        self.assertIn(b'Title and author are required!', response.data)

    # Тест доступа к несуществующей книге
    def test_access_nonexistent_book(self):
        response = self.app.get('/book/999', follow_redirects=True)  # 999 - предположительно несуществующий ID
        self.assertEqual(response.status_code, 404)

    # Тест успешного удаления книги
    def test_delete_book_successfully(self):
        with app.app_context():
            book = Book(title='Book to Delete', author='Author', description='Description')
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.app.get(f'/delete/{book_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            deleted_book = Book.query.get(book_id)
            self.assertIsNone(deleted_book)

    # Тест обработки невалидных данных при добавлении книги
    def test_add_invalid_book(self):
        response = self.app.post('/add_book', data=dict(
            title='',  # пустое название
            author='Test Author',
            description='Test Description',
            genre='Test Genre'
        ), follow_redirects=True)
        self.assertIn(b'Title and author are required!', response.data)

    # Тест доступа к несуществующей книге
    def test_access_nonexistent_book(self):
        response = self.app.get('/book/999', follow_redirects=True)  # 999 - предположительно несуществующий ID
        self.assertEqual(response.status_code, 404)

    # Тест успешного удаления книги
    def test_delete_book_successfully(self):
        with app.app_context():
            book = Book(title='Book to Delete', author='Author', description='Description')
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.app.get(f'/delete/{book_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            deleted_book = Book.query.get(book_id)
            self.assertIsNone(deleted_book)

    # Тест поиска книги
    def test_search_book(self):
        # Добавим книгу для тестирования
        with app.app_context():
            book = Book(title='Search Book', author='Author', description='Description')
            db.session.add(book)
            db.session.commit()

        response = self.app.post('/search', data=dict(
            search_term='Search Book'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Book', response.data)

    # Тест удаления книги
    def test_delete_book(self):
        # Добавим книгу для тестирования
        with app.app_context():
            book = Book(title='Delete Book', author='Author', description='Description')
            db.session.add(book)
            db.session.commit()

        book_id = Book.query.first().id

        response = self.app.get(f'/delete/{book_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Book', response.data)

if __name__ == '__main__':
    unittest.main()
