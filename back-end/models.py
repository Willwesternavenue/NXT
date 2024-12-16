from app import db

class User(db.Model):
    __tablename__ = 'users'  # 明示的にテーブル名を指定

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # データベースに合わせて 'name' に変更

    def __repr__(self):
        return f'<User {self.name}>'
