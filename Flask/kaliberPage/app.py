from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import openai
import os
import datetime

# Program skrivet av Charlie Rosander

app = Flask(__name__, static_url_path='/static')

current_time = datetime.datetime.now()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
openweathermap_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
app.secret_key = 'hejhopp'

weather_images = {
    'clear sky': 'https://openweathermap.org/img/wn/01d@2x.png',
    'few clouds': 'https://openweathermap.org/img/wn/02d@2x.png',
    'scattered clouds': 'https://openweathermap.org/img/wn/03d@2x.png',
    'broken clouds': 'https://openweathermap.org/img/wn/04d@2x.png',
    'overcast clouds': 'https://openweathermap.org/img/wn/04d@2x.png',
    'shower rain': 'https://openweathermap.org/img/wn/09d@2x.png',
    'rain': 'https://openweathermap.org/img/wn/10d@2x.png',
    'light rain': 'https://openweathermap.org/img/wn/10d@2x.png',
    'thunderstorm': 'https://openweathermap.org/img/wn/11d@2x.png',
    'snow': 'https://openweathermap.org/img/wn/13d@2x.png',
    'fog': 'https://openweathermap.org/img/wn/50d@2x.png'
}


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route("/signup")
def sign_up():
    return render_template('signup.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route("/home")
def home_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    city_query = request.args.to_dict()
    city = city_query.get('city', 'Stockholm')

    if not city:
        return render_template('home.html')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}&units=metric'
    response = requests.get(url).json()

    try:
        temperature = response['main']['temp']
        description = response['weather'][0]['description']
        country = response['sys']['country']
        location = f'{city}, {country}'
        feels_like = response['main']['feels_like']
        image = weather_images.get(description, None)
    except (KeyError, IndexError):
        return render_template('home.html')

    current_user = None
    if 'user_id' in session:
        current_user = User.query.filter_by(id=session['user_id']).first()
    return render_template('home.html', location=location, temperature=temperature, description=description, feels_like=feels_like, image=image, current_user=current_user)


@app.route('/chatgpt')
def chatgpt_page():
    return render_template("chatgpt.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{user_message}",
        temperature=0.8,
        max_tokens=3500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    gpt_response = response.choices[0].text.strip()
    return str(gpt_response)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route('/contact')
def contact_page():
    return render_template("contact.html")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


def create_tables():
    db.create_all()


with app.app_context():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)
