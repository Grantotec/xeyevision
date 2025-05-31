from app import create_app, db
from flask_migrate import Migrate
from app.auth.models import User  # Добавляем явный импорт моделей
from app.admin.models import Event

app = create_app()
migrate = Migrate(app, db)

from app import create_app, db
from app.auth.models import User
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
