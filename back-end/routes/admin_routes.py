from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, AdminUser, Client
from forms import AdminLoginForm, ClientCreateForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.client_list'))
    return render_template('admin_login.html', form=form)

@admin_bp.route('/client-list')
def client_list():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    clients = Client.query.all()
    return render_template('client_list.html', clients=clients)

@admin_bp.route('/create-client', methods=['GET', 'POST'])
def create_client():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    form = ClientCreateForm()
    if form.validate_on_submit():
        new_client = Client(
            company=form.company.data,
            contact_name=form.contact_name.data,
            login_id=form.login_id.data,
            login_password=form.login_password.data,
            credit_balance=0
        )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('admin.client_list'))
    return render_template('client_create.html', form=form)
