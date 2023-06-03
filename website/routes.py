from website import app, admin_user
from flask import render_template, redirect, url_for, flash, request, Response
from flask_uploads import UploadSet, configure_uploads, IMAGES
from website.Forms import *
from website.models import *
from flask_login import login_user,logout_user, login_required, current_user
import re
import shelve
from werkzeug.utils import secure_filename
import PIL
import os
from uuid import uuid1
#from flask_recaptcha import ReCaptcha
from markupsafe import Markup
#csrf
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
import cryptography 
from cryptography.fernet import Fernet
class csrfform(FlaskForm):
    country_name = StringField('country_name')   
#end csrf
bcrypt = Bcrypt()
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
photos = UploadSet('photos', IMAGES)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  

def configure_app(app):
    configure_uploads(app, photos)


def check_password_strength(password):
    if len(password) < 8:
        flash("Password is too short, at least 8 characters, try again", category='danger')
        return False
    elif re.search("[a-z]", password) is None:
        flash("Password is missing a lowercase letter, try again", category='danger')
        return False
    elif re.search("[A-Z]", password) is None:
        flash("Password is missing a uppercase letter, try again", category='danger')
        return False
    elif re.search("[0-9]", password) is None:
        flash("Password is missing a digit, try again", category='danger')
        return False
    elif re.search("[!@#\$%^&*()_\-+=\{\}\[\]:;\"'<>,.?/|\\~`]", password) is None:
        flash("Password is missing a special character, try again.", category='danger')
        return False
    else:
        return "True"


@app.route('/')
def index():
    csrf = csrfform()
    users = User.query.all()
    try:
        item_list = []
        item_db = shelve.open('website/databases/items/items.db', 'r')
        products_database = shelve.open('website/databases/products/products.db', 'c')
        if 'ItemInfo' in item_db:
            Items_Dict = item_db['ItemInfo']
            
            for key in Items_Dict:
                item = Items_Dict.get(key)
                item_list.append(item)
            item_db.close()
        else:
            item_db['ItemInfo'] = Items_Dict
            item_db.close()

    except IOError:
        print("Unable to Read File", item_list=item_list)

    except Exception as e:
        print(f"An unknown error has occurred,{e}")
    return render_template('index.html', item_list=item_list, users=users)

@app.route('/user_management/disable/<int:id>', methods=['POST'])
@login_required
def user_disable(id):
    userID = User.query.filter_by(id=id).first()
    userID.status = 'Disabled'
    flash(f'{userID.username} account has been disabled', category='danger')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/user_management/enable/<int:id>', methods=['POST'])
@login_required
def user_enable(id):
    userID = User.query.filter_by(id=id).first()
    userID.status = 'Enabled'
    flash(f"{userID.username} account has been enabled", category='success')
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/login_page', methods=["GET", "POST"])
def login_page():
    admin_user()
    form = LoginForm()
    csrf = csrfform()
    if form.validate_on_submit() and request.method=="POST":
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # if user exist and if password is correct
            attempted_user = User.query.filter_by(username=form.username.data).first()
            if attempted_user.status == 'Enabled':
                login_user(attempted_user)
                flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
                return redirect(url_for('index'))
            else:
                flash(f"{attempted_user.username} account has been disabled!" f" Please contact Customer Support for more information.", category='danger')
                #return redirect(url_for('login_page'))
        else:
            flash("Invalid username or password, please try again.", category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register_page():
    db.create_all()
    form = RegisterForm()
    csrf = csrfform()
    if request.method == "POST":
        password = request.form.get('password1')
        if check_password_strength(password) == False:
            return redirect(url_for('register_page'))
        else:
                if form.validate_on_submit():
                    user_to_create = User(username=form.username.data,
                                        email_address=form.email_address.data,
                                        password=form.password1.data,
                                        usertype="customers")
                    # 'password' = form.password1.data this is entering the hashed
                    # version of the password. Check models.py,
                    # @password.setter hashes the passwords
                    db.session.add(user_to_create)
                    db.session.commit()
                    login_user(user_to_create)
                    flash(f"Success! You are logged in as: {user_to_create.username}", category='success')

                    return redirect(url_for('index'))
                if form.errors != {}:  # If there are not errors from the validations
                    errors = []
                    for err_msg in form.errors.values():
                        errors.append(err_msg)
                    err_message = '<br/>'.join(
                        [f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
                    flash(f'{err_message}', category='danger')

    return render_template('register.html', form=form)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home_page():
    csrf = csrfform()
    userID = User.query.filter_by(id=current_user.id).first()
    return render_template('home.html')

@app.route('/image/<int:id>')
def get_img(id):

    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)



@app.route('/admin', methods=["GET", "POST"])
@login_required
def landing_pagea():
    admin_user()

    db.create_all()
    # warning very funny error when logging in if passwords are not hashed(check SQlite) it will crash
    # giving an error of Invalid salt Value error
    form = LoginForm()
    csrf = csrfform()
    if form.validate_on_submit():
        # if user exist and if password is correct
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            if attempted_user.account_availability(attempted_user.status) == "sven":
                return redirect(url_for('home_page'))
            elif attempted_user.account_availability(attempted_user.status) != 0:
                # checks username for valid user and checks if password is correct
                login_user(attempted_user)
                if current_user.usertype != 'customers':
                    if current_user.usertype == 'retailers':
                        flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
                        return redirect(url_for('retail_homepage'))
                    else:
                        flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
                        return redirect(url_for('home_page'))
                else:
                    logout_user()
                    flash(f"This login page is for admins, staff & retailers.  ", category='danger')
                    return redirect(url_for('landing_pagea'))
            else:
                flash(f"{attempted_user.username} account has been disabled!"
                      f" Please contact Customer Support for more information.", category='danger')
        else:
            flash("Username or Password are not matched! Please try again.", category='danger')
    
    return render_template('admin_login.html', form=form)


@app.route('/professional', methods=["GET", "POST"])
@login_required
def pro_login():
    admin_user()

    db.create_all()
    # warning very funny error when logging in if passwords are not hashed(check SQlite) it will crash
    # giving an error of Invalid salt Value error
    form = LoginForm()
    if form.validate_on_submit():
        # if user exist and if password is correct
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            if attempted_user.account_availability(attempted_user.status) == "sven":
                return redirect(url_for('home_page'))
            elif attempted_user.account_availability(attempted_user.status) != 0:
                # checks username for valid user and checks if password is correct
                login_user(attempted_user)
                if current_user.usertype != 'customers':
                    # 'login_user' is a built-in function for flask_login
                    flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
                    if current_user.usertype == "retailers":
                        return redirect(url_for('retail_homepage'))
                    else:
                        return redirect(url_for('home_page'))
                else:
                    logout_user()
                    flash(f"If you are a customer, please login to the customer login page side. ", category='danger')
                    return redirect(url_for('pro_login'))
            else:
                flash(f"{attempted_user.username} account has been disabled!"
                      f" Please contact Customer Support for more information.", category='danger')
        else:
            flash("Username or Password are not matched! Please try again.",
                  category='danger')

    return render_template('professional_login.html', form=form)


@app.route('/market')
@login_required
def market_place():
    csrf = csrfform()
    item_list = []
    try:
        item_db = shelve.open('website/databases/items/items.db', 'r')
        products_database = shelve.open('website/databases/products/products.db', 'c')
        if 'ItemInfo' in item_db:
            Items_Dict = item_db['ItemInfo']
            for key in Items_Dict:
                item = Items_Dict.get(key)
                item_list.append(item)
            item_db.close()
        else:
            item_db['ItemInfo'] = Items_Dict
            item_db.close()

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")


    return render_template('market.html', item_list=item_list)

@app.route('/sell', methods=['POST', 'GET'])
@login_required
def sell():
    add_item_form = ListItemForm()
    your_products_dict = {}
    Items_Dict = {}
    image_dict = {}
    image_list = []

    
    #unique_id = uuid4()
    try:
        item_db = shelve.open('website/databases/items/items.db', 'c')
        Your_Products_Database = shelve.open('website/databases/products/products.db', 'c')
        image_location_db = shelve.open('website/databases/items/images.db', 'c')
        
        if 'ItemInfo' in item_db:
            Items_Dict = item_db['ItemInfo']
        else:
            item_db['ItemInfo'] = Items_Dict
            
        if str(current_user.id) in Your_Products_Database:
            your_products_dict = Your_Products_Database[str(current_user.id)]
        else:
            Your_Products_Database[str(current_user.id)] = your_products_dict
        
    except IOError:
        flash("Unable to Read File", category='danger')

    except Exception as e:
        flash(f"An unknown error has occurred,{e}", category='danger')

    else:
        if request.method == 'POST':
            
            pic = request.files['pic']

            if not pic:
                flash("Please Insert an Image before adding a product.", category='danger')
                return redirect(url_for('sell'))
        
   
            id = 0
           

            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype

            while True:
                #unique_id = uuid4()
                id += 1
                if str(id) not in Items_Dict:
                    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
                    db.session.add(img)
                    db.session.commit()
                    file = pic.filename
                   
                    

                    #img = Item_Img(img=pic_name)
                    #db.session.add(img)
                    #saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                    #db.session.commit()
                    item = Product(owner=current_user.username, owner_id=current_user.id, name=add_item_form.product_name.data, price=add_item_form.pricing.data, brand=add_item_form.brand.data, category=add_item_form.category.data, title=add_item_form.listing_title.data, deal_method=add_item_form.deal_method.data, description=add_item_form.description.data, mass=add_item_form.mass.data, image=img.id)
                    item.set_id(id)
                    Items_Dict[str(id)] = item
                    your_products_dict[str(id)] = item
                    item_db['ItemInfo'] = Items_Dict
                    Your_Products_Database[str(current_user.id)] = your_products_dict
                    flash('Item Added Successfully', category='success')
                    print('Item added')
                    item_db.close()
                    Your_Products_Database.close()
                
                    return redirect(url_for('index'))
                else:
                    continue

    return render_template('sell.html', add_item_form=add_item_form), 200


@app.route('/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy_item(id):
    buy_item_form = Purchase_Form()
    Items_Dict = {}
    Owned_Items_Dict = {}

    try:
        item_db = shelve.open('website/databases/items/items.db', 'r')
        Owned_Items_Database = shelve.open('website/databases/Owned_Items/ownedItems.db', 'c')
        if 'ItemInfo' in item_db:
            Items_Dict = item_db['ItemInfo']
        else:
            item_db['ItemInfo'] = Items_Dict

        
        if str(current_user.id) in Owned_Items_Database:
            Owned_Items_Dict = Owned_Items_Database[str(current_user.id)]
            print(Owned_Items_Database[str(current_user.id)])
        else:
            Owned_Items_Database[str(current_user.id)] = Owned_Items_Dict

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")



@app.route('/deleteItem/<id>', methods=['GET', 'POST'])
def delete_item(id):
    item_dict = {}
    item_db = shelve.open('website/databases/items/items.db', 'w')
    item_dict = item_db['ItemInfo']

    item_dict.pop(id)

    item_db['ItemInfo'] = item_dict
    item_db.close()

    return redirect(url_for('market_place'))


@app.route('/updateItem/<id>', methods=['GET', 'POST'])
def update_item(id):
    update_item_form = UpdateItemForm()
    item_dict = {}
    image_dict = {}
    image_list = []

    try:
        item_db = shelve.open('website/databases/items/items.db', 'w')
        if 'ItemInfo' in item_db:
            item_dict = item_db['ItemInfo']
        else:
            item_db['ItemInfo'] = item_dict

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")

    else:
        if request.method == "POST":
            item = item_dict.get(id)

            pic = request.files['pic']

            if not pic:
                flash("Please Insert an Image before adding a product.", category='danger')
                return redirect(url_for('update_item', id=id))
            
            file = pic.filename
            image_dict[id] = file

            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype


            img = Img(img=pic.read(), mimetype=mimetype, name=filename)
            db.session.add(img)
            db.session.commit()


            item.set_name(update_item_form.product_name.data)
            item.set_img(img.id)
            item.set_title(update_item_form.listing_title.data)
            item.set_description(update_item_form.description.data)
            item.set_price(update_item_form.pricing.data)
            item.set_mass(update_item_form.mass.data)



            item_db['ItemInfo'] = item_dict
            item_db.close()

            return redirect(url_for('market_place'))
        else:
            
            item = item_dict.get(id)
            #update_item_form.item_pic.data = img
            update_item_form.product_name.data = item.get_name()
            update_item_form.listing_title.data = item.get_title()
            update_item_form.description.data = item.get_description()
            update_item_form.pricing.data = item.get_price()
            update_item_form.mass.data = item.get_mass()



        
    return render_template('update_item.html', update_item_form=update_item_form)


        
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    id = User.query.filter_by(id=current_user.id).first()
    return render_template('profile.html')


@app.route('/update_profile_pic', methods=['GET', 'POST'])
@login_required
def update_profile_pic():
    update_profile_pic_form = Update_Profile_Pic()
    if request.method == 'POST':
        userID = User.query.filter_by(id=current_user.id).first()
        # Check for profile pic
        if request.files['profile_pic'] and allowed_file(request.files['profile_pic'].filename):
            userID.profile_pic = request.files['profile_pic']

            # Grab Image Name
            pic_filename = secure_filename(userID.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['profile_pic']

            # Change it to a string to save to db
            userID.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("Profile pic Updated Successfully!", category='success')
                return redirect(url_for("profile_page"))

            except:
                if update_profile_pic_form.errors != {}:  # If there are not errors from the validations
                    errors = []
                    for err_msg in update_profile_pic_form.errors.values():
                        errors.append(err_msg)
                    err_message = '<br/>'.join(
                        [f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
                    flash(f'{err_message}', category='danger')
            return redirect(url_for('profile_page'))
        else:
            flash('Filetype not supported, only png, jpg and jpeg are supported.', category='danger')
            return redirect(url_for('profile_page'))


@app.route("/updateDescription", methods=["GET", "POST"])
def update_description():
    form = Update_User_Description()
    userID = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST" and form.validate_on_submit():
        print("form: ", form.description.data)
        userID.description = form.description.data
        db.session.commit()
        flash("Description updated", category='success')
        return redirect(url_for('profile_page'))
    return render_template("UpdateDescription.html", form=form, user=current_user.id)



@app.route('/admin/customer_management', methods=['GET', 'POST'])
def customer_management():
    users = User.query.all()
    print(users[0].username)
    
@app.route('/forget_password')
def forgot_password():
    return render_template('forgot.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html')

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('error/429.html')

@app.errorhandler(403)
def perms_error(e):
  return render_template('error/403.html')