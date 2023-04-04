Pizza Shop

This is a simple web application for a pizza shop using Flask, SQLite, and pandas. Users can register, log in, view the menu, view their profile (including order history), edit their contact information and place orders. The admin user can manage pizzas, orders and delete users.

Features

    User registration and login
    Guest-login (no registration required), with limited functionality
    Database for users, orders and pizzas, using SQLite and SQLAlchemy with password hashing using Werkzeug
    Admin user management
    Pizza menu management (add, edit, delete pizzas)
    Place orders (add items to cart and checkout)
    View and manage orders (admin only)
    Profile page for both admin and users (view and edit contact info and view order history)

Requirements

    Python
    Flask
    Flask-SQLAlchemy
    pandas
    python-dotenv
    Werkzeug

Installation

Run the app with docker, using:
 ```
 docker run -d -p 5000:5000 kaliber123/theperfectslice
 ```
 
Usage

    Register a new user, log in as an existing user (or as the admin) or continue as guest (Some features, like order history is for regisered users only).
    Browse the menu and add items to the cart.
    Proceed to the cart, review your order, and click on "Checkout" to place an order.
    When a order is marked as done by the admin, the customer can view the order in their profile page, aswell as see their contact-information.
    Admin can manage pizzas (add, edit, delete) and orders (view, mark as done, delete) from the menu and orders pages, respectively. Aswell as deleting users from the database.


Structure

    app.py: Main application file containing the Flask application and routes.
    database.db: SQLite database containing tables for users, orders, and pizzas.
    Docs/menu.csv: CSV file containing the pizza menu.
    templates/: Folder containing the HTML templates for the application.
    .env: Environment variables file, containing the admin login.

License
Created by Charlie Rosander.
This project is licensed under the MIT License.