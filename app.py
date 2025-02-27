from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
import os
import pymongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
connection = pymongo.MongoClient(os.getenv('MONGO'))
print(os.getenv('MONGO'))
db = connection['BookReviewProject']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db.User.find_one({
        '_id': ObjectId(user_id)
    })

    return User(user)

class User(UserMixin):
    def __init__(self, user):
        self.id = str(user['_id'])
        self.name = user['name']
        self.username = user['username']
        self.password = user['password']


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Name"})
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.User.find_one({
            'username': username.data
        })

        if user:
            raise ValidationError('Username already exists')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit() and form.validate_username(form.username.data):
        hashed_password = Bcrypt().generate_password_hash(form.password.data)

        user = {
            'name': form.name.data,
            'username': form.username.data,
            'password': hashed_password
        }

        db.User.insert_one(user)
        return redirect(url_for('home'))

    return render_template('registration.html', form=form)
#24:38
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("HELLO HELLO")
        user = db.User.find_one({
            'username': form.username.data
        })
        
        if user and Bcrypt().check_password_hash(user['password'], form.password.data):
            print(f'User {user["username"]} logged in')
            print(user)
            what = login_user(User(user))
            print(what)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run()