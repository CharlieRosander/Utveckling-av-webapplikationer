from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import openai
import os
import datetime

app = Flask(__name__, static_url_path='/static')

current_time = datetime.datetime.now()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
openweathermap_api_key = os.getenv('OPENWEATHERMAP_API_KEY')

weather_images = {
    'clear sky': 'https://openweathermap.org/img/wn/01d@2x.png',
    'few clouds': 'https://openweathermap.org/img/wn/02d@2x.png',
    'scattered clouds': 'https://openweathermap.org/img/wn/03d@2x.png',
    'broken clouds': 'https://openweathermap.org/img/wn/04d@2x.png',
    'shower rain': 'https://openweathermap.org/img/wn/09d@2x.png',
    'rain': 'https://openweathermap.org/img/wn/10d@2x.png',
    'thunderstorm': 'https://openweathermap.org/img/wn/11d@2x.png',
    'snow': 'https://openweathermap.org/img/wn/13d@2x.png',
}

@app.route("/")
@app.route("/home")
def home_page():
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
        return render_template('error.html')

    return render_template('home.html', location=location, temperature=temperature, description=description, feels_like=feels_like, image=image)

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

if __name__ == "__main__":
    app.run(debug=True)
