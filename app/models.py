import decimal
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120),
                                             index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    incomes: so.WriteOnlyMapped['Income'] = so.relationship(back_populates='recipient')
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(back_populates='spender')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def total_income(self) -> decimal.Decimal:
        return db.session.scalar(
            sa.select(sa.func.sum(Income.amount))
            .where(Income.user_id == self.id)
        ) or decimal.Decimal('0.00')


@login.user_loader
def load_user(user_id: int) -> User:
    return db.session.get(User, user_id)

class Income(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    amount: so.Mapped[decimal.Decimal] = so.mapped_column(sa.DECIMAL(10,2))
    income_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.Date())
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    recipient: so.Mapped[User] = so.relationship(back_populates='incomes')

    def __repr__(self):
        return '<Income {} - {}>'.format(self.name, self.amount)

class Expense(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    amount: so.Mapped[decimal.Decimal] = so.mapped_column(sa.DECIMAL(10,2))
    expense_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.Date())
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    spender: so.Mapped[User] = so.relationship(back_populates='expenses')

    def __repr__(self):
        return '<Expense {} - {}>'.format(self.name, self.amount)