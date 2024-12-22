from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from forms import UserCreateForm, LoginForm, AdminLoginForm, AdminCreateForm
from decimal import Decimal

import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ローカルとDocker環境で適切な .env ファイルを読み込む
if os.environ.get('FLASK_ENV') == 'docker':
    load_dotenv('.env.docker')  # Docker 環境用の設定を読み込む
else:
    load_dotenv('.env.local')  # ローカル開発環境用の設定を読み込む
# 環境変数を読み込み

# 環境変数からデータベース接続情報を取得
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'admin')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'adminpass')}@"
    f"{os.getenv('POSTGRES_HOST', 'db')}:"
    f"{os.getenv('POSTGRES_PORT', 5432)}/"
    f"{os.getenv('POSTGRES_DB', 'NXT-DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')  # CSRFのためのセッションキー

# SQLAlchemy と Flask-Migrate の初期化
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ログ設定: エラー以上のログのみ表示
logging.basicConfig(level=logging.ERROR)

# ユーザーモデル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  
    password = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)  
    credit_balance = db.Column(db.Numeric(10, 2), default=0.00)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.before_request
def clear_session_messages():
    """不要なセッションメッセージを削除する"""
    if session.get('messages'):
        session.pop('messages')

@app.route('/test-db', methods=['GET'])
def test_db():
    """データベース接続テストエンドポイント"""
    try:
        users = User.query.all()
        return jsonify([user.name for user in users])
    except Exception as e:
        app.logger.error(f"Database query failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/admin-create', methods=['GET', 'POST'])
def admin_create():
    form = AdminCreateForm()

    if request.method == 'POST':  # POSTリクエストの場合のみエラーメッセージを表示
        if form.validate_on_submit():
            admin_name = form.name.data
            admin_password = form.password.data
            
            # ハッシュ化されたパスワードを生成
            hashed_password = generate_password_hash(admin_password)

            # 新しいadminユーザーを作成
            new_admin = Admin(name=admin_name, password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()

            flash('Admin user created successfully!', 'success')
            return redirect(url_for('admin_create'))
        else:
            app.logger.error(f"Form errors: {form.errors}")
            flash('Form validation failed.', 'danger')

    return render_template('admin_create.html', form=form)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserCreateForm()

    if form.validate_on_submit():
        try:
            app.logger.debug(f"Form data: company={form.company.data}, name={form.name.data}, password={form.password.data}")
        
            # パスワードをハッシュ化
            hashed_password = generate_password_hash(form.password.data)

            # 新しいユーザーを作成（name と company のマッピング）
            new_user = User(
                name=form.name.data,  # name フィールドを使用
                password=hashed_password,
                company=form.company.data,  # company フィールドを使用
                credit_balance=0.00  # credit_balance のデフォルトはすでに 0.00 なので明示的に設定
            )

            # データベースに追加
            db.session.add(new_user)
            db.session.commit()

            # データベースに保存されたユーザーを確認
            user = User.query.filter_by(name=new_user.name).first()
            app.logger.debug(f"Created user: {user.name}, {user.company}, {user.credit_balance}")

            flash('User created successfully!', 'success')
            return redirect(url_for('create_user'))  # フォームをリセットして再表示

        except Exception as e:
            db.session.rollback()  # エラーが発生した場合、ロールバックする
            app.logger.error(f"Error creating user: {e}")
            flash(f"Error creating user: {e}", 'danger')
            return redirect(url_for('create_user'))

    return render_template('client_create.html', form=form)

# ログイン用ルート
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        # ログイン状態であれば、直接ダッシュボードにリダイレクト
        flash('You are already logged in!', 'info')
        return redirect(url_for('admin_dashboard'))

    form = AdminLoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data).first()

        if admin and check_password_hash(admin.password, form.password.data):
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('admin_login.html', form=form)

@app.route('/admin-logout')
def admin_logout():
    if session.get('admin_logged_in'):
        session.pop('admin_logged_in', None)
        # ログアウトメッセージを設定
        flash('Logged out successfully!', 'success')
    else:
        flash('You are not logged in.', 'warning')
    
    # フラッシュメッセージのみを設定し、リダイレクト先で処理
    return redirect(url_for('admin_login'))


# 管理者用ダッシュボード
@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # CompanyNameの昇順で並べる
    users = User.query.order_by(User.company).all()  # Userテーブルのcompanyカラムで昇順にソート

    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            charge_amount = request.form.get('charge_amount')
            
            # charge_amountをDecimal型に変換
            charge_amount = Decimal(charge_amount)

            user = User.query.get(user_id)

            if user:
                # credit_balanceもDecimal型なので直接加算可能
                user.credit_balance += charge_amount
                db.session.commit()
                flash(f'Credit balance updated for {user.name}', 'success')
            else:
                flash(f'User with ID {user_id} not found.', 'danger')
        except ValueError:
            flash('Invalid amount entered. Please enter a valid number for charge.', 'danger')
        except Exception as e:
            app.logger.error(f"Error occurred: {e}")
            flash('An unexpected error occurred. Please try again later.', 'danger')
    
    return render_template('admin_dashboard.html', users=users)


# クライアントログイン用のフォームとルートを追加
@app.route('/client-login', methods=['GET', 'POST'])
def client_login():
    form = LoginForm()

    if request.method == 'POST':  # POSTリクエストの場合のみエラーメッセージを表示
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.login_id.data).first()
            if user and check_password_hash(user.password, form.password.data):
                flash('Login successful!', 'success')
                return redirect(url_for('create_user'))  # ログイン後にユーザー作成ページにリダイレクト
            else:
                flash('Login failed. Check your login credentials and try again.', 'danger')
        else:
            flash('Form validation failed.', 'danger')

    return render_template('client-login.html', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
