from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Client, SimPurchase
from forms import ClientLoginForm
from datetime import datetime

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/login', methods=['GET', 'POST'])
def client_login():
    form = ClientLoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(login_id=form.login_id.data, login_password=form.login_password.data).first()
        if client:
            session['client_id'] = client.id
            return redirect(url_for('client.purchase_sim'))
    return render_template('client_login.html', form=form)

@client_bp.route('/purchase-sim', methods=['GET', 'POST'])
def purchase_sim():
    # 簡略化のため、固定プランを想定
    if 'client_id' not in session:
        return redirect(url_for('client.client_login'))

    client_id = session['client_id']
    client = Client.query.get(client_id)

    if request.method == 'POST':
        plan_name = request.form.get('plan_name')
        cost = int(request.form.get('cost', 0))

        if client.credit_balance >= cost:
            client.credit_balance -= cost
            purchase = SimPurchase(client_id=client.id, plan_name=plan_name, cost=cost)
            db.session.add(purchase)
            db.session.commit()
            return "Purchase successful!"
        else:
            return "Not enough credit!"

    # サンプルのプラン
    plans = [
        {"name": "Plan A", "cost": 10},
        {"name": "Plan B", "cost": 20}
    ]
    return render_template('purchase_sim.html', client=client, plans=plans)
