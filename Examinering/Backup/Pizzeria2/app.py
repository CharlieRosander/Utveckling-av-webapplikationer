from flask import Flask, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'secretkey'

#### CSV ####
def read_csv_file():
    df = pd.read_csv("./Docs/menu.csv")
    return df
    #### /CSV ####


#### DATABASE ####
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model admin table #
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

# Model table for users #
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

# Create admin user func #
def create_admin():
    admin = Admin.query.filter_by(username='admin').first()
    if admin is None:
        admin = Admin(username='admin', password='123')
        db.session.add(admin)
        db.session.commit()

# Create tables func #
def create_tables():
    db.create_all()

# Call create_tables and admin funcs #
with app.app_context():
    create_tables()
    create_admin()
#### /DATABASE ####


#### REGISTER ####
@app.route("/signup")
def sign_up():
    return render_template('signup.html')

# Add user to database #
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    flash(f"User: {new_user.username} created successfully.", 'success')
    return redirect(url_for('login'))
#### /REGISTER ####

#### LOGIN ####
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        user = User.query.filter_by(username=username).first()

        if admin:
            if admin.password == password:
                session['user'] = admin.username
                flash(f"Successfully logged in as: {session['user']}.", 'success')
                return redirect(url_for('index'))

        if user:
            if check_password_hash(user.password, password):
                session['user'] = user.username
                flash(f"Successfully logged in as: {session['user']}.", 'success')
                return redirect(url_for('index'))
            else:
                error = 'Incorrect password, try again.'

        else:
            error = 'Username does not exist.'

    return render_template('login.html', error=error)

#### /LOGIN ####

#### LOGOUT ####
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop("guest", None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))
#### /LOGOUT ####

#### PAGE ROUTES ####
@app.route('/index')
def index():
    if not session.get('user'):
        session['user'] = 'guest'
    if not session.get('cart'):
        session['cart'] = json.dumps([])
    return render_template('index.html')

@app.route('/menu')
def menu():
    if not session.get('cart'):
        session['cart'] = json.dumps([])

    cart = json.loads(session['cart'])

    df = read_csv_file()
    column_names = list(df.columns.values)  # Convert column names to a list
    row_data = df.values.tolist()
    return render_template("menu.html", column_names=column_names, row_data=row_data, cart=cart)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/cart')
def cart():
    if not session.get('cart'):
        session['cart'] = json.dumps([])
    cart = json.loads(session['cart'])

    return render_template('cart.html', cart=cart)

# Add pizza to cart #
@app.route('/add_to_cart/<int:pizza_id>', methods=['POST'])
def add_to_cart(pizza_id):
    df = read_csv_file()
    pizza = df.loc[df['id'] == pizza_id].to_dict(orient='records')[0]
    pizza['Quantity'] = int(request.form.get('quantity', 1))
    cart = json.loads(session['cart'])

    # Check if the pizza is already in the cart
    for item in cart:
        if item['id'] == pizza['id']:
            item['Quantity'] += pizza['Quantity']
            break
    else:
        cart.append(pizza)

    flash(f"{pizza['Quantity']}x {pizza['Name']} added to cart")
    session['cart'] = json.dumps(cart)
    return redirect(url_for('menu'))

# Remove pizza from cart #
@app.route('/remove_from_cart/<int:pizza_id>', methods=['POST'])
def remove_from_cart(pizza_id):
    cart = json.loads(session['cart'])

    for index, item in enumerate(cart):
        if item['id'] == pizza_id:
            cart.pop(index)
            break

    session['cart'] = json.dumps(cart)
    flash("Item removed from cart")

    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = json.dumps([])
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = json.loads(session['cart'])
    return render_template('checkout.html', cart=cart)

@app.route('/add_pizza', methods=['GET', 'POST'])
def add_pizza():
    if request.method == 'POST':
        df = read_csv_file()
        pizza_id = df["id"].max() + 1
        pizza_df = pd.DataFrame(columns=['id', 'name', 'price', 'size', 'toppings'])
        pizza_df = pizza_df.append({'id': pizza_id, 'name': request.form['name'], 'price': request.form['price'],
                                     'size': request.form['size'], 'toppings': request.form['toppings']}, ignore_index=True)
        
        pizza_df.to_csv('Docs/menu.csv', mode='a', header=False, index=False)

        return redirect(url_for('menu'))
    return render_template('add_pizza.html')
#### /PAGE ROUTES ####

# Run app #
if __name__ == '__main__':
    app.run(debug=True)
