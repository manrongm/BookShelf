from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
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
db = connection['BookReviewProject']
books_collection = db['books']
reading_plans_collection = db['reading_plans']
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

    def validate_username(self, username1):
        user = db.User.find_one({
            'username': username1.data
        })

        if user:
            raise ValidationError('Username already exists')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/')
def home():
    books = list(books_collection.find())
    print(books)
    return render_template('index.html', books = books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        year = request.form.get('year')
        rating = request.form.get('rating')
        review = request.form.get('review')

        book_data = {
            'title': title,
            'author': author,
            'genre': genre,
            'year': year,
            'rating': rating,
            'review': review
        }

        books_collection.insert_one(book_data)
        flash('Book added successfully!', 'success')

        return redirect(url_for('home'))

    return render_template('add_book.html')

@app.route('/delete_book/<book_id>', methods=['POST'])
def delete_book(book_id):
    result = books_collection.delete_one({'_id': ObjectId(book_id)})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 400
    
@app.route('/edit_book/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = books_collection.find_one({'_id': ObjectId(book_id)})
    
    if request.method == 'POST':
        updated_data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'genre': request.form.get('genre'),
            'year': request.form.get('year'),
            'rating': request.form.get('rating'),
            'review': request.form.get('review')
        }
        books_collection.update_one({'_id': ObjectId(book_id)}, {'$set': updated_data})
        flash('Book updated successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('edit_book.html', book=book)

@app.route('/reading_plans')
def reading_plans():
    plans = list(reading_plans_collection.find())

    for plan in plans:
        book_details = []
        books_read = 0
        for book in plan['books']:
            book_info = books_collection.find_one({'_id': ObjectId(book['book_id'])})
            if book_info:
                book_details.append({
                    'book_id': book['book_id'],
                    'title': book_info['title'],
                    'read': book['read']
                })
                if book['read']:
                    books_read += 1 
        
        plan['books'] = book_details
        plan['books_read'] = books_read
        plan['total_books'] = len(book_details)

    return render_template('reading_plan.html', plans=plans)


@app.route('/delete_reading_plan/<plan_id>', methods=['POST'])
def delete_reading_plan(plan_id):
    result = reading_plans_collection.delete_one({'_id': ObjectId(plan_id)})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 400
    
@app.route('/add_reading_plan', methods=['GET', 'POST'])
def add_reading_plan():
    if request.method == 'POST':
        name = request.form.get('name')
        due_date = request.form.get('due_date')
        selected_books = request.form.getlist('books')

        reading_plan = {
            'name': name,
            'due_date': due_date,
            'books': [{'book_id': book_id, 'read': False} for book_id in selected_books]
        }
        reading_plans_collection.insert_one(reading_plan)
        return redirect(url_for('reading_plans'))
    
    books = list(books_collection.find())
    return render_template('add_plan.html', books=books)

@app.route('/update_reading_plan/<plan_id>', methods=['POST'])
def update_reading_plan(plan_id):
    plan = reading_plans_collection.find_one({'_id': ObjectId(plan_id)})
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404

    book_id = request.form.get('book_id')

    updated_books = []
    for book in plan['books']:
        if book['book_id'] == book_id:
            book['read'] = not book.get('read', False)  # Toggle read status
        updated_books.append(book)

    reading_plans_collection.update_one(
        {'_id': ObjectId(plan_id)}, 
        {'$set': {'books': updated_books}}
    )

    return jsonify({'success': True, 'updated_books': updated_books})

@app.route('/get_reading_plan/<plan_id>', methods=['GET'])
def get_reading_plan(plan_id):
    plan = reading_plans_collection.find_one({'_id': ObjectId(plan_id)})

    if not plan:
        return jsonify({'error': 'Plan not found'}), 404

    book_details = []
    books_read = 0
    for book in plan['books']:
        book_info = books_collection.find_one({'_id': ObjectId(book['book_id'])})
        if book_info:
            book_details.append({
                'book_id': book['book_id'],
                'title': book_info['title'],
                'read': book['read']
            })
            if book['read']:
                books_read += 1

    return jsonify({
        'name': plan['name'],
        'books': book_details,
        'books_read': books_read,
        'total_books': len(book_details)
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        form.validate_username(form.username)
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
        user = db.User.find_one({
            'username': form.username.data
        })
        
        if user and Bcrypt().check_password_hash(user['password'], form.password.data):
            login_user(User(user))
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
