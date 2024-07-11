from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Dummy check for example purposes
    if username == 'admin' and password == 'password':
        session['username'] = username
        return redirect(url_for('success'))
    else:
        flash('Login Failed. Please check your username and password.')
        return redirect(url_for('home'))

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
