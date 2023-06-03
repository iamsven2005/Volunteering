from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp, NumberRange
from website.models import *
from flask_wtf.recaptcha import RecaptchaField


class RegisterForm(FlaskForm):
    #username validation
    recaptcha = RecaptchaField()

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    #email address validation
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    #checks if the user has met all the conditions with their credentials in creating their account
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    #takes in input from the user of their login credentials
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class ListItemForm(FlaskForm):
    category = SelectField(u'Select a category... ', choices=[('fr', 'Fruits'), ('vg', 'Vegetables'), ('sc', 'Sauce/condiments'), ('mt', 'Plant-based meat'), ('sn', 'Plant-based snacks'), ('dm', 'Dim-sum')], default='Select category... ')
    product_name = StringField('Name of product: ', validators=[DataRequired(), ])
    listing_title = StringField(label="Listing title: ", validators=[DataRequired()])
    pricing = DecimalField(label='S$', places=2, rounding=None, use_locale=False, number_format=None)
    description = TextAreaField(label="Description: ")
    brand = StringField(label='Brand: ', validators=[Length(min=2, max=30)])
    mass = DecimalField(label='Mass: ', places=2, rounding=None, use_locale=False, number_format=None)
    deal_method = SelectField(label='Deal method: ', choices=[('1', 'Meet-up'), ('2', 'Delivery')])
    item_pic = FileField("Product Pic")
    submit = SubmitField(label="List now")


class UpdateItemForm(FlaskForm):
    category = SelectField(u'Select a category... ', choices=[('fr', 'Fruits'), ('vg', 'Vegetables'), ('sc', 'Sauce/condiments'), ('mt', 'Plant-based meat'), ('sn', 'Plant-based snacks'), ('dm', 'Dim-sum')], default='Select category... ')
    product_name = StringField('Name of product: ', validators=[DataRequired(), ])
    listing_title = StringField(label="Listing title: ", validators=[DataRequired()])
    pricing = DecimalField(label='S$', places=2, rounding=None, use_locale=False, number_format=None)
    description = TextAreaField(label="Description: ")
    brand = StringField(label='Brand: ', validators=[Length(min=2, max=30)])
    mass = DecimalField(label='Mass: ', places=2, rounding=None, use_locale=False, number_format=None)
    deal_method = SelectField(label='Deal method: ', choices=[('1', 'Meet-up'), ('2', 'Delivery')])
    item_pic = FileField("Product Pic")
    submit = SubmitField(label="Update list")


class Add_To_Cart_Form(FlaskForm):
    quantity = IntegerField(label="Quantity To Add", validators=[
                            NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Add to Cart')

class Purchase_Form(FlaskForm):
    quantity = IntegerField(label="Quantity To Add", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Add to Cart')



class Update_User(FlaskForm):
    username = StringField(label='User Name:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    profile_pic = FileField("Profile Pic")
    submit = SubmitField(label='Update Account')

class Update_Profile_Pic(FlaskForm):
    profile_pic = FileField("Profile Pic")
    submit = SubmitField(label='Done')

class Update_User_Description(FlaskForm):
    description = TextAreaField("About User")
    submit = SubmitField(label='Update Description')