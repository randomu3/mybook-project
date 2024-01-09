# extensions.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Создаем экземпляр приложения Flask
app = Flask(__name__)
# Устанавливаем URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# Отключаем отслеживание модификаций, чтобы избежать предупреждения
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Создаем экземпляр SQLAlchemy для работы с базой данных

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy(app)