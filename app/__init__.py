import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
session = Session()
login_manager = LoginManager()

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOADED_FILES_DEST'] = 'app/uploads/proofs'

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    session.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from . import models, routes, forms
        db.create_all()
    return app