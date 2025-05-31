from app import create_app, db
from app.auth.models import User
from app.admin.models import Event

app = create_app()

with app.app_context():
    db.create_all()
    print("Таблицы базы данных успешно созданы!")