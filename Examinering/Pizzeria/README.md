Pizza Shop

This is a simple web application for a pizza shop using Flask, SQLite, and pandas. Users can register, log in, view the menu, view their profile (including order history) and place orders. The admin user can manage pizzas and orders.
Features

    User registration and login
    Guest-login (no registration required), with limited functionality
    Database for users, orders and pizzas, using SQLite and SQLAlchemy with password hashing using Werkzeug
    Admin user management
    Pizza menu management (add, edit, delete pizzas)
    Place orders (add items to cart and checkout)
    View and manage orders (admin only)
    Profile-page for both admin and users (view contact info and order history)

Requirements

    Python 3.6 or higher
    Flask
    Flask-SQLAlchemy
    pandas
    python-dotenv
    Werkzeug

Installation

    Clone the repository:

bash

git clone https://github.com/yourusername/pizza-shop.git

    Change directory:

bash

cd pizza-shop

    Create a virtual environment:

python3 -m venv venv

    Activate the virtual environment:

bash

source venv/bin/activate

    Install the required packages:

pip install -r requirements.txt

    Set up environment variables in a .env file:

makefile

ADMIN_USERNAME=<your_admin_username>
ADMIN_PASSWORD=<your_admin_password>

    Run the application:

python app.py

    Access the application at http://localhost:5000

Usage

    Register a new user, log in as an existing user (or as the admin) or continue as guest (Some features, like order-history is for regisered users only).
    Browse the menu and add items to the cart.
    Proceed to the cart, review your order, and click on "Checkout" to place an order.
    When a order is marked as done by the admin, the customer can view the order in their profile page, aswell as see their contact-information.
    Admin can manage pizzas (add, edit, delete) and orders (view, mark as done, delete) from the menu and orders pages, respectively.


Structure

    app.py: Main application file containing the Flask application and routes.
    database.db: SQLite database containing tables for users, orders, and pizzas.
    Docs/menu.csv: CSV file containing the pizza menu.
    templates/: Folder containing the HTML templates for the application.
    .env: Environment variables file (not included in the repository, create your own).

License
Created by Charlie Rosander.
This project is licensed under the MIT License.