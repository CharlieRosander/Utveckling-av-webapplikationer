# Pizza Shop

Pizza Shop is a web application built with Flask, SQLite, and pandas. It allows users to register, log in, view the menu, place orders, and manage their profile, while the admin can manage pizzas, orders, and users. The application features password hashing with Werkzeug and uses SQLAlchemy for database management.

## Features

- User registration and login
- Guest-login (no registration required), with limited functionality
- Database for users, orders and pizzas, using SQLite and SQLAlchemy with password hashing using Werkzeug
- Admin user management
- Pizza menu management (add, edit, delete pizzas)
- Place orders (add items to cart and checkout)
- View and manage orders (admin only)
- Profile page for both admin and users (view and edit contact info and view order history)

## Requirements

- Python
- Flask
- Flask-SQLAlchemy
- pandas
- python-dotenv
- Werkzeug

## Installation

1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`
3. Run the app with `python app.py`

## Usage

1. Register a new user, log in as an existing user (or as the admin) or continue as a guest. Some features, like order history, are only available for registered users.
2. Browse the menu and add items to the cart.
3. Proceed to the cart, review your order, and click on "Checkout" to place an order.
4. When an order is marked as done by the admin, the customer can view the order in their profile page, as well as see their contact-information.
5. Admin can manage pizzas (add, edit, delete) and orders (view, mark as done, delete) from the menu and orders pages, respectively. They can also delete users from the database.

## Structure

- `app.py`: Main application file containing the Flask application and routes.
- `database.db`: SQLite database containing tables for users, orders, and pizzas.
- `docs/menu.csv`: CSV file containing the pizza menu.
- `templates/`: Folder containing the HTML templates for the application.
- `.env`: Environment variables file, containing the admin login.

## License

Created by Charlie Rosander. This project is licensed under the MIT License.
