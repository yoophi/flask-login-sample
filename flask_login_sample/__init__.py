from datetime import datetime

from flask import Flask

from flask_login_sample.config import ConfigClass
from flask_login_sample.database import db
from flask_login_sample.models import User, Role
from flask_login_sample.user import user_manager


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(ConfigClass)

    db.init_app(app)

    # Setup Flask-User and specify the User data-model
    user_manager.init_app(app, db, User)

    init_blueprint(app)
    init_commands(app)

    return app


def init_blueprint(app):
    from .views import main as main_bp
    app.register_blueprint(main_bp)


def init_commands(app):
    @app.cli.command('init-db')
    def init_db():
        db.create_all()

        # Create 'member@example.com' user with no roles
        if not User.query.filter(User.email == 'member@example.com').first():
            user = User(
                email='member@example.com',
                email_confirmed_at=datetime.utcnow(),
                password=user_manager.hash_password('Password1'),
            )
            db.session.add(user)
            db.session.commit()

        # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
        if not User.query.filter(User.email == 'admin@example.com').first():
            user = User(
                email='admin@example.com',
                email_confirmed_at=datetime.utcnow(),
                password=user_manager.hash_password('Password1'),
            )
            user.roles.append(Role(name='Admin'))
            user.roles.append(Role(name='Agent'))
            db.session.add(user)
            db.session.commit()
