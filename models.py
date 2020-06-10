from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

users_orders_association = db.Table(
    "users_orders",
    db.Column("user_id", db.Integer, db.ForeignKey("users.ID")),
    db.Column("chat_id", db.Integer, db.ForeignKey("orders.ID")),
)

meals_orders_association = db.Table(
    "meals_orders",
    db.Column("meals_id", db.Integer, db.ForeignKey("meals.ID")),
    db.Column("orders_id", db.Integer, db.ForeignKey("orders.ID")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("ID", db.Integer, primary_key=True)
    mail = db.Column('Mail', db.String, nullable=False)
    password_hash = db.Column('Password', db.String, nullable=False)
    order = db.relationship('Order', secondary=users_orders_association, back_populates='user')

    @property
    def password(self):
        # Запретим прямое обращение к паролю
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        # Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        # Проверяем пароль через этот метод
        # Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column('ID', db.Integer, primary_key=True)
    title = db.Column('Title', db.String, nullable=False)
    meals = db.relationship("Meal", back_populates='category')


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column('ID', db.Integer, primary_key=True)
    title = db.Column('Title', db.String, nullable=False)
    picture = db.Column("Picture", db.String, nullable=False)
    price = db.Column('Price', db.Integer, nullable=False)
    description = db.Column('Description', db.String, nullable=False)
    category = db.relationship('Category', back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.ID'))
    orders = db.relationship('Order',
                             secondary=meals_orders_association,
                             back_populates='meals')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column('ID', db.Integer, primary_key=True)

    data = db.Column('Data', db.String, nullable=False)
    summa = db.Column('Summa', db.Integer, nullable=False)
    phone = db.Column("Phone", db.String, nullable=False)
    address = db.Column('Address', db.String, nullable=False)

    user = db.relationship('User',
                           secondary=users_orders_association,
                           back_populates='order')
    meals = db.relationship('Meal',
                            secondary=meals_orders_association,
                            back_populates='orders')
