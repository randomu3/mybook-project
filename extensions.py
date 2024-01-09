# extensions.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр приложения Flask
app = Flask(__name__)
# Устанавливаем URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# Создаем экземпляр SQLAlchemy для работы с базой данных
db = SQLAlchemy(app)