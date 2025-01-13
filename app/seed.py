from models import User, Tovar, Zakaz, Address
from main import db


def seeds():
    data = User(name="Vasiliy", is_active=True)
    data.set_password('111')
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
