from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = "supersecretkey"

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models 

    from app.routes import students_bp
    app.register_blueprint(students_bp)
    from app.routes import courses_bp
    app.register_blueprint(courses_bp)
    from app.routes import instructors_bp
    app.register_blueprint(instructors_bp)
    from app.routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes import grades_bp
    app.register_blueprint(grades_bp)

    return app 