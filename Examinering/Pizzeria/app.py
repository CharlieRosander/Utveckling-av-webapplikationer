from flask import Flask, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#### DATABASE ####
class User(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if admin is None:
        admin = User(username='admin', password='123')
        db.session.add(admin)
        db.session.commit()

def create_tables():
    db.create_all()

with app.app_context():
    create_tables()
    create_admin()
#### /DATABASE ####

#### LOGIN ####
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    current_user = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.username == username and user.password == password:
                session['user_id'] = user.id
                current_user = User.query.filter_by(id=session['user_id']).first()
                flash('Logged in successfully.')
                return redirect(url_for('index'))
            else:
                error = ('Incorrect password, try again.')
        else:
            error = ('Username does not exist.')
    return render_template('login.html', error=error, current_user=current_user)
#### /LOGIN ####

@app.route('/index')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
