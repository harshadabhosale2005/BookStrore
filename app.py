from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory user store (for demo)
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return f"✅ Login successful! Welcome, {username}."
        else:
            error = '❌ Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = '⚠️ Username already exists!'
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
