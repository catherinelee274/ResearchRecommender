# run.py

from flask import Flask
app = Flask(__name__)

@app.route('/')
def generalRecommend():
    #recommends based on what you've clicked/upload'
    #infinite scrolling
    #general recommendation 
    return 'Hello, World!'

@app.route('/upload')
def paperRecommend():
    #uploads all this to a database 
    return 'Recommends'