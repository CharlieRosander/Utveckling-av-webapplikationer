from flask import Flask, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


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

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


def create_admin():
    admin = Admin.query.filter_by(username='admin').first()
    if admin is None:
        admin = Admin(username='admin', password='123')
        db.session.add(admin)
        db.session.commit()

def create_tables():
    db.create_all()

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
        
        if "guest" in request.form:
            session["user"] = "guest"
            return redirect(url_for('index'))

        elif admin:
            if admin.password == password:
                session["user"] = admin.username
                return redirect(url_for('index'))

        elif user:
            if check_password_hash(user.password, password):
                session["user"] = user.username
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
    flash('Logged out successfully.')
    return redirect(url_for('login'))
#### /LOGOUT ####

#### PAGE ROUTES ####
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    df = read_csv_file()
    column_names = list(df.columns.values)  # Convert column names to a list
    row_data = df.values.tolist()
    return render_template("menu.html", column_names=column_names, row_data=row_data)


@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
#### /PAGE ROUTES ####

if __name__ == '__main__':
    
    app.run(debug=True)
