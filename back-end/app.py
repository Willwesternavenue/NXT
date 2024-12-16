from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

# 環境変数を読み込み
load_dotenv()

# Flask アプリケーションの初期化
app = Flask(__name__)

# 環境変数からデータベース接続情報を取得
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'admin')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'adminpass')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', 5432)}/"
    f"{os.getenv('POSTGRES_DB', 'NXT-DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy と Flask-Migrate の初期化
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ログ設定: エラー以上のログのみ表示
logging.basicConfig(level=logging.ERROR)

# テーブルモデルの定義
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/test-db', methods=['GET'])
def test_db():
    """データベース接続テストエンドポイント"""
    try:
        users = User.query.all()
        return jsonify([user.name for user in users])
    except Exception as e:
        app.logger.error(f"Database query failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Flask アプリケーションの起動
    app.run(host="0.0.0.0", port=5002)

