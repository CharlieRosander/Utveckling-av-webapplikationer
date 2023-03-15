from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/charl/Desktop/AI-Developer-Jensen/Utveckling-av-webapplikationer/Flask/flaskDBapp/instance/test.db'
app.config['SECRET_KEY'] = "dev"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

def create_db():
    db.create_all()


if __name__ == "__main__":
    create_db()
    db.create_all()
    app.run(Debug=True)
    