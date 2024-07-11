from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random JWT secret key

jwt = JWTManager(app)

# In-memory user database for demonstration with hashed passwords
users = {
    "Joseph": generate_password_hash("password")
}

@app.route('/')
def home():
    return 'Welcome to the Home Page! <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug prints
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Check if the username exists and the password matches asfdasdf fsdfdsf h second coomiut

        

        if username in users and check_password_hash(users[username], password):
            print("Login successful")
            access_token = create_access_token(identity=username)
            flash('Login successful!')
            return redirect(url_for('home'))  # Redirect to home after successful login
        else:
            print("Invalid username or password")
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username in users and check_password_hash(users[username], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
