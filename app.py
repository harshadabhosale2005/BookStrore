from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "bookstore"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bookstore_db'

mysql = MySQL(app)

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )

        user = cur.fetchone()

        if user:

            session['user_id'] = user[0]
            session['user_name'] = user[1]

            return redirect('/')

        else:
            return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        cur = mysql.connection.cursor()

        # check email already exists
        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            return "Email already registered"

        # insert new user
        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name,email,password)
        )

        mysql.connection.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


@app.route('/cart')
def cart():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template('cart.html')


@app.route('/wishlist')
def wishlist():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template('wishlist.html')

@app.route('/checkout', methods=['GET','POST'])

def checkout():

    if request.method == 'POST':

        address = request.form['address']
        payment = request.form['payment']

        return redirect('/order_success')

    return render_template('checkout.html')

@app.route('/order')
def order():

    if 'user_id' not in session:
        return redirect('/login')

    book = request.args.get('book')
    price = request.args.get('price')

    return render_template(
        'order.html',
        book=book,
        price=price
    )

@app.route('/place_order', methods=['POST'])
def place_order():

    if 'user_id' not in session:
        return redirect('/login')

    fullname = request.form['fullname']
    mobile = request.form['mobile']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']

    payment = request.form['payment']

    book = request.form['book']
    price = request.form['price']

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    cur.execute(
        """
        INSERT INTO orders
        (
            user_id,
            fullname,
            mobile,
            address,
            city,
            state,
            book_name,
            price,
            payment_method
        )

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,

        (
            user_id,
            fullname,
            mobile,
            address,
            city,
            state,
            book,
            price,
            payment
        )
    )

    mysql.connection.commit()

    return redirect('/order_success')

@app.route('/order_success')
def order_success():

    return render_template('order_success.html')

@app.route('/geobook')
def geobook():
    return render_template('geobook.html')


@app.route('/biobook')
def biobook():
    return render_template('biobook.html')


@app.route('/historybook')
def historybook():
    return render_template('historybook.html')

if __name__ == '__main__':
    app.run(debug=True)