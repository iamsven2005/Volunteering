from website import bcrypt
from website import db, login_manager
from datetime import datetime
import random
import string
from uuid import uuid4
import shelve
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    retailer_id = db.Column(db.Integer())
    staff_id = db.Column(db.Integer())
    admin = db.Column(db.Integer())
    usertype = db.Column(db.String(120))
    # the id unique to each user so that flask can identify each individual user
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60),
                              nullable=False, unique=True)
    profile_pic = db.Column(db.String(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    # the mostly used hashing algorithm that flask allow us to use
    # will always convert the passwords to being 60 characters
    # thats why length is set to 60
    date = db.Column(db.String(), default=datetime.now().strftime("%d/%m/%Y"))
    budget = db.Column(db.Integer(), nullable=False, default=10000)
    gender = db.Column(db.String(), nullable=False, default='Rather not say')
    messages = db.Column(db.Integer(), nullable=False, default=0)
    # items = db.relationship('Item', backref='owned_user', lazy=True)
    # relationship is to make it so some items have some relationship to
    # the user.
    shoppingCartCount = db.Column(db.Integer(), nullable=False, default=0)
    profits = db.Column(db.Integer(), nullable=False, default=0)
    spending = db.Column(db.Integer(), nullable=False, default=0)
    #profile_pic = db.Column(db.String(),nullable=True)

    # Account status (Adds 'Disabled' or 'Enabled' status column to User Database)
    status = db.Column(db.Integer(), nullable=False, default='Enabled')

    @property
    def password(self):
        return self.password

    # return password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    # hashes the password entered by users creating new accounts

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        # return true or false

    def can_deposit(self, deposit_to_check):
        return deposit_to_check > 0

    def account_availability(self, status):
        if status == "Disabled":
            return 0

    # Password Reset Function
    def password_otp(self, size=8, chars=string.ascii_uppercase + string.digits):
        otp = ''.join(random.choice(chars) for _ in range(size))
        return otp

    # Make sure otp cannot be reused again.
    def scramble_otp(self, size=128, chars=string.ascii_uppercase + string.digits):
        otp = ''.join(random.choice(chars) for _ in range(size))
        return otp
    

class Product:
    def __init__(self, owner, owner_id, name, price, description, brand, mass, category, deal_method, title, image):
        self.__id = 0
        self.__name = name
        self.__title = title
        self.__condition = None
        self.__price = price
        self.__description = description
        self.__brand = brand
        self.__mass = mass
        self.__owner = owner
        self.__owner_id = owner_id
        self.__category = category
        self.__deal_method = deal_method
        self.__date_purchased = None
        self.__qty_purchased = None
        self.__total_cost = None
        self.__image = image
        self.__owner = None

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id
    
    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_img(self, img):
        self.__image = img

    def get_img(self):
        return self.__image
    
    def set_owner(self, owner):
        self.__owner = owner
        
    def get_owner(self):
        return self.__owner
    
    def set_title(self, title):
        self.__title = title
    
    def get_title(self):
        return self.__title
    
    def set_condition(self, condition):
        self.__condition = condition

    def get_condition(self):
        return self.__condition
    
    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description
    
    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price
    
    def set_mass(self, mass):
        self.__mass = mass

    def get_mass(self):
        return self.__mass
    

    
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class Item_Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(), nullable=False)

