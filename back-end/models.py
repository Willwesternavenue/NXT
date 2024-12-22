from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100))
    company = db.Column(db.String(100))
    credit_balance = db.Column(db.Numeric(10, 2), default=0.00)  # クレジット残高 (USD)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)  # 会社名
    contact_name = db.Column(db.String(100), nullable=False)  # 担当者名
    name = db.Column(db.String(50), unique=True, nullable=False)  # ログインID -> name
    password = db.Column(db.String(100), nullable=False)  # パスワード -> password
    credit_balance = db.Column(db.Numeric(10, 2), default=0.00)  # クレジット残高 (USD)

    # リレーションシップ
    sim_purchases = db.relationship('SimPurchase', backref='client', lazy=True)

    def __repr__(self):
        return f'<Client {self.name}>'

class SimPurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.name}>'
