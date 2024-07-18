from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Flag to ensure tables are created only once
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True
        logging.debug("Database tables created.")

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logging.error("Username or password missing in request.")
            return jsonify({'error': 'Username and password are required.'}), 400

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            logging.debug(f"User registered: {username}")
            return jsonify({'message': 'Registration successful! You can now log in.', 'redirect': url_for('home')})
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            db.session.rollback()  # Rollback the session in case of error
            return jsonify({'error': 'Registration failed. Username might already be taken.'}), 400
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logging.error("Username or password missing in request.")
            return jsonify({'error': 'Username and password are required.'}), 400

        user = User.query.filter_by(username=username).first()

        if user:
            logging.debug(f"User found: {user.username}")
            logging.debug(f"Stored hash: {user.password}")
            if check_password_hash(user.password, password):
                session['username'] = user.username
                logging.debug(f"Login successful for user: {user.username}")
                return jsonify({'redirect': url_for('success')})
            else:
                logging.debug("Password does not match.")
                return jsonify({'error': 'Login Failed. Please check your username and password.'}), 400
        else:
            logging.debug("User not found.")
            return jsonify({'error': 'Login Failed. Please check your username and password.'}), 400
    return render_template('login.html')

@app.route('/success')
def success():
    if 'username' in session:
        return render_template('success.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
