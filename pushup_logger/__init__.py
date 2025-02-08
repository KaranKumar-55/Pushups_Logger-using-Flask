from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from . import models  # Ensure models are imported

    with app.app_context():
        db.create_all()


    Login_Manager = LoginManager()
    Login_Manager.login_view = 'auth.login'
    Login_Manager.init_app(app)

    from .models import User
    @Login_Manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))



    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

