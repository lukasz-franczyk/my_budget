from flask import render_template, flash, redirect, url_for, request
from app import db
import sqlalchemy as sa
from flask_login import current_user, login_required
from app.main.forms import IncomesForm
from app.models import User, Income
from app.utils import str_to_datetime
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = db.first_or_404(sa.select(User).where(User.id == current_user.id))
    query = user.incomes.select()
    incomes = db.session.scalars(query)

    sum_incomes = user.total_income()

    return render_template('index.html', title='Home', incomes=incomes, sum_incomes=sum_incomes)


@bp.route('/incomes', methods=['GET', 'POST'])
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
        return redirect(url_for('main.incomes'))
    return render_template('incomes.html', title='Incomes', form=form)

