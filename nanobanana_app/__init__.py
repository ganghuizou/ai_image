from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('nanobanana_app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    from . import auth
    auth.init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        from . import models
        db.create_all()

    return app