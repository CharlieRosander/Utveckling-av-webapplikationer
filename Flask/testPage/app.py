from flask import Flask, render_template, url_for, request
import requests
import openai
import os
import datetime
import pytz
from dotenv import load_dotenv


app = Flask(__name__, static_url_path='/static')

load_dotenv()
# openai.api_key = os.environ["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"]
# openai.api_key = "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"


@app.route("/")
@app.route("/home")
def home_page():
    # Make API request to OpenWeather API
    api_key = '8aa9225c5c2b6bfa6519474cf42233f9'
    city_query = request.args.to_dict()
    city = city_query.get('city', 'Stockholm')

    if not city:
        return render_template('home.html')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url).json()

    # Extract relevant weather data from API response
    temperature = response['main']['temp']
    description = response['weather'][0]['description']
    country = response['sys']['country']
    location = f'{city}, {country}'
    temperature = response['main']['temp']
    description = response['weather'][0]['description']
    feels_like = response['main']['feels_like']

    # choose the appropriate weather image based on the description
    if 'clear sky' in description:
        image = 'https://openweathermap.org/img/wn/01d@2x.png'
    elif 'few clouds' in description:
        image = 'https://openweathermap.org/img/wn/02d@2x.png'
    elif 'scattered clouds' in description:
        image = 'https://openweathermap.org/img/wn/03d@2x.png'
    elif 'broken clouds' in description:
        image = 'https://openweathermap.org/img/wn/04d@2x.png'
    elif 'shower rain' in description:
        image = 'https://openweathermap.org/img/wn/09d@2x.png'
    elif 'rain' in description:
        image = 'https://openweathermap.org/img/wn/10d@2x.png'
    elif 'thunderstorm' in description:
        image = 'https://openweathermap.org/img/wn/11d@2x.png'
    elif 'snow' in description:
        image = 'https://openweathermap.org/img/wn/13d@2x.png'
    else:
        image = None

    return render_template('home.html', location=location, temperature=temperature, description=description, feels_like=feels_like, image=image)


@app.route('/chatgpt')
def chatgpt_page():
    return render_template("chatgpt.html")


@app.route('/chat', methods=['POST'])
def chat():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Get user input message from form
    message = request.form['message']

    # Generate response using OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Return response to frontend
    return str(response.choices[0].text)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route('/contact')
def contact_page():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(Debug=True)
