from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class IncomesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    income_date  = StringField('Income date : YYYY-MM-DD')
    submit = SubmitField('Add income')

class ExpensesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    expense_date  = StringField('Expense date : YYYY-MM-DD')
    submit = SubmitField('Add expense')