from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
# from .views import SecureModelView
from flask_admin.contrib.sqla import ModelView


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'S00pre seAkr3t pass'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vuln_app.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        # NOTE: this may allow user enumeration once logged in
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for administrative tasks
    admin = Admin(app, name='Vulnerable App', template_mode='bootstrap3')
    # admin.add_view(SecureModelView(User, db.session))
    admin.add_view(ModelView(User, db.session))

    return app