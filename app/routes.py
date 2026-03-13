from flask import render_template, flash, redirect, url_for, request
from app import app ,db
import sqlalchemy as sa
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm, IncomesForm
from app.models import User, Income
from urllib.parse import urlsplit
from datetime import datetime
import decimal
from app.utils import str_to_datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = db.first_or_404(sa.select(User).where(User.id == current_user.id))
    query = user.incomes.select()
    incomes = db.session.scalars(query)

    sum_incomes = user.total_income()

    return render_template('index.html', title='Home', incomes=incomes, sum_incomes=sum_incomes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
    form = IncomesForm()
    if form.validate_on_submit():
        date_obj = str_to_datetime(form.income_date.data)
        income = Income(name=form.name.data, amount=form.amount.data, income_date=date_obj,
                        user_id=current_user.id)

        db.session.add(income)
        db.session.commit()
        flash('Income added!')
        return redirect(url_for('incomes'))
    return render_template('incomes.html', title='Incomes', form=form)

