from datetime import datetime, timezone, date
from app import db
from app.models import Income


def str_to_datetime(date_string : str) -> date:
    return datetime.fromisoformat(date_string).date()



if __name__ == '__main__':
    date_string = '2026-11-30'
    date_obj = str_to_datetime(date_string)
    print(type(date_obj))
    print(date_obj)
