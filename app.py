from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415

    data = request.get_json()
    """username=request.form("username")
    username=request.form("password")"""
    
    username = data.get("username")
    password = data.get("password")
    
    
    global_api_url = 'https://example.com/api/login'
    api_response = requests.post(global_api_url, json=data)
    
    
    if username == 'admin' and password == 'p':
        session['username'] = username
        return jsonify({'redirect': url_for('success')})
    else:
        flash('Login Failed. Please check your username and password.')
        return jsonify({'redirect': url_for('home')})

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
