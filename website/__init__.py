from flask import Flask, render_template, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from dotenv import load_dotenv
from os import path
import os
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
DB_NAME = 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # if database.db does not exist in this path it creates a database
        with app.app_context():
            db.create_all()
            print('Created Database! ')


bcrypt = Bcrypt(app)


def admin_user():
    from website.models import User
    db.create_all()
    with app.app_context():
        admin = User(admin=1, username='admin', password='admin123',
                     email_address='admin@example.com', gender='rather not say')

        if not User.query.filter_by(admin=admin.id).first() and not User.query.filter_by(email_address=admin.email_address).first() and not User.query.filter_by(username=admin.username).first():
            db.session.add(admin)
            db.session.commit()

            # dexter the admin thing is here

create_database(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'info'


UPLOAD_FOLDER = 'website/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from website import routes