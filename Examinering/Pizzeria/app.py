from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import json
import os

app = Flask(__name__)
app.secret_key = 'secretkey'
load_dotenv()

#### CSV ####
def read_csv_file():
    df = pd.read_csv("./Docs/menu.csv")
    return df
#### /CSV ####

#### DATABASE ####
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB admin table #
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

# DB table for users #
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    address = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    date = db.Column(db.String(80), nullable=False)

# DB table for orders #
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    items = db.relationship('OrderItems', cascade="all, delete", backref='order')

# Sub table for orders #
class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    pizza = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

# DB table for completed orders
class CompletedOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('CompletedOrderItems', cascade="all, delete", backref='completed_order')

# Sub table for completed orders
class CompletedOrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed_order_id = db.Column(db.Integer, db.ForeignKey('completed_orders.id'), nullable=False)
    pizza = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

# Create admin user func #
def create_admin():
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    hashed_password = generate_password_hash(admin_password)

    admin = Admin.query.filter_by(username=admin_username).first()
    if admin is None:
        admin = Admin(username=admin_username, password=hashed_password)
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
    try:
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            address = request.form['address']
            phone = request.form['phone']
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, date=date)

            # Add email, address, and phone if they have a value
            if email:
                new_user.email = email
            if address:
                new_user.address = address
            if phone:
                new_user.phone = phone

            db.session.add(new_user)
            db.session.commit()

        else:
            flash(f"User: {user.username} already exists.", 'danger')
            return redirect(url_for('sign_up'))

        flash(f"User: {new_user.username} created successfully.", 'success')
        return redirect(url_for('login'))
    
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while adding the user: {str(e)}", 'danger')
        return redirect(url_for('sign_up'))
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

        
        if admin and check_password_hash(admin.password, password):
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
    session.pop("cart", None)
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
    if 'user' not in session or session['user'] == 'guest':
        flash("Please log in to view your profile.")
        return redirect(url_for('login'))

    if 'admin' in session['user']:
        current_user = Admin.query.filter_by(username=session['user']).first()
    
    else:
        current_user = User.query.filter_by(username=session['user']).first()

    if current_user is None:
        flash("User not found. Please log in again.")
        return redirect(url_for('login'))

    complete_orders = CompletedOrders.query.filter_by(username=current_user.username).all()
   
    return render_template('profile.html', current_user=current_user, complete_orders=complete_orders)

@app.route('/edit_contact_info', methods=['GET', 'POST'])
def edit_contact_info():
    if 'user' not in session or session['user'] == 'guest':
        # Redirect to login page if the user is not logged in
        return redirect(url_for('login'))

    current_user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        # Update the user's contact information in the database only if the field is not empty
        if username:
            old_username = current_user.username
            current_user.username = username

            # Update the username in the CompletedOrders table
            completed_orders = CompletedOrders.query.filter_by(username=old_username).all()
            for order in completed_orders:
                order.username = username

        if email:
            current_user.email = email
        if phone:
            current_user.phone = phone
        if address:
            current_user.address = address

        db.session.commit()

        # Update the session variable
        session['user'] = current_user.username

        flash('Your contact information has been updated.', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', current_user=current_user)


#### CART ####
@app.route('/cart')
def cart():
    if not session.get('cart'):
        session['cart'] = json.dumps([])
    cart = json.loads(session['cart'])

    return render_template('cart.html', cart=cart)

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

# Clear cart #
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = json.dumps([])
    flash("Cart cleared")
    return redirect(url_for('cart'))

# Checkout #
@app.route('/checkout', methods=['POST'])
def checkout():
    session_data = json.loads(session.get('cart'))

    if not session_data:
        flash('Your cart is empty. Please add items before checking out.', 'warning')
        return redirect(url_for('menu'))
    
    total_price = sum([d['Price'] * d['Quantity'] for d in session_data])
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    order = Orders(username=session['user'], date=date)
    db.session.add(order)
    db.session.flush()  # This is needed to get the generated order id

    order_df = pd.DataFrame(session_data)
    for _, row in order_df.iterrows():
        order_item = OrderItems(order_id=order.id, pizza=row['Name'], price=row['Price'],
                                quantity=row['Quantity'], total=total_price)
        db.session.add(order_item)

    db.session.commit()

    session.pop('cart', None)
    flash('Your order has been placed. Thank you for shopping with us!', 'success')
    return redirect(url_for('menu'))
#### /CART ####

#### MANAGE PIZZAS ####
# Add new pizza #
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

# Edit existing pizza #
@app.route('/edit_pizza/<int:pizza_id>', methods=['GET', 'POST'])
def edit_pizza(pizza_id):
    df = read_csv_file()
    pizza = df.loc[df['id'] == pizza_id].to_dict(orient='records')[0]

    if request.method == 'POST':
        updated_name = request.form['name'] or pizza['Name']
        updated_price = request.form['price'] or pizza['Price']
        updated_size = request.form['size'] or pizza['Size']
        updated_toppings = request.form['toppings'] or pizza['Toppings']

        update_pizza_by_id(pizza_id, updated_name, updated_price, updated_size, updated_toppings)
        flash(f"Pizza with ID {pizza_id} has been updated.")
        return redirect(url_for('menu'))

    return render_template('edit_pizza.html', pizza=pizza)

# Update existing pizza #
def update_pizza_by_id(pizza_id, name, price, size, toppings):
    df = pd.read_csv('./Docs/menu.csv')

    # Find the row with the given ID and update its values
    df.loc[df['id'] == pizza_id, 'Name'] = name
    df.loc[df['id'] == pizza_id, 'Price'] = price
    df.loc[df['id'] == pizza_id, 'Size'] = size
    df.loc[df['id'] == pizza_id, 'Toppings'] = toppings

    # Write the updated DataFrame to the CSV file
    df.to_csv('./Docs/menu.csv', index=False)

# Delete existing pizza #
@app.route('/delete_pizza/<int:pizza_id>', methods=['POST'])
def delete_pizza(pizza_id):
    df = pd.read_csv('./Docs/menu.csv')

    # Find the row with the given ID and delete it
    df = df[df['id'] != pizza_id]

    # Write the updated DataFrame to the CSV file
    df.to_csv('./Docs/menu.csv', index=False)

    flash(f"Pizza with ID {pizza_id} has been deleted.")
    return redirect(url_for('menu'))
#### /MANAGE PIZZAS ####

#### ORDERS ####
@app.route('/orders')
def orders():

    if session.get('user') == 'admin':
        orders = Orders.query.all()
        return render_template('orders.html', orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/get_order_items/<int:order_id>')
def get_order_items(order_id):
    items = OrderItems.query.filter_by(order_id=order_id).all()
    items_data = []
    for item in items:
        item_data = {
            'pizza': item.pizza,
            'price': item.price,
            'quantity': item.quantity,
            'total': item.total
        }
        items_data.append(item_data)
    return jsonify(items_data)

# Delete an order
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Orders.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f"Order with ID {order_id} has been deleted.")
    return redirect(url_for('orders'))

# Mark an order as done
@app.route('/mark_order_as_done/<int:order_id>', methods=['POST'])
def mark_order_as_done(order_id):
    order = Orders.query.get(order_id)
    total_price = db.select(OrderItems.total).where(OrderItems.order_id == order_id)

    # Save the order details in the CompletedOrders and CompletedOrderItems tables
    completed_order = CompletedOrders(username=order.username, date=order.date, total_price=total_price)
    db.session.add(completed_order)
    db.session.flush()

    order_items = OrderItems.query.filter_by(order_id=order_id).all()
    for item in order_items:
        completed_order_item = CompletedOrderItems(completed_order_id=completed_order.id, pizza=item.pizza, price=item.price, quantity=item.quantity, total=item.total)
        db.session.add(completed_order_item)

    # Mark the order as completed in the Orders table
    order.completed = True
    db.session.commit()

    flash(f"Order with ID {order_id} has been marked as done.")
    return redirect(url_for('orders'))
#### /ORDERS ####

#### MANAGE USERS ####
# Get all users #
@app.route('/users')
def users():
    if session.get('user') == 'admin':
        all_users = User.query.all()
        return render_template('users.html', all_users=all_users)
    else:
        flash("You are not authorized to view this page.")
        return redirect(url_for('login'))

# Remove a user #
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User with ID {user_id} has been deleted.")
    return redirect(url_for('users'))
#### /PAGE ROUTES ####

# Run app #
if __name__ == '__main__':
    app.run(debug=True)
