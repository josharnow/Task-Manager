# __init__.py
from flask import Flask # Import Flask to allow us to create our app by importing the Flask class; from the flask package we import the Flask class
app = Flask(__name__) # Create a new instance of the Flask class called "app"
app.secret_key = "root"