# utils/db_utils.py
from app import db
from app.models import User

def create_database():
    db.create_all()
    print("База данных успешно создана")

if __name__ == '__main__':
    create_database()