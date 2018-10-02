from flask import Flask,render_template,request, make_response
import json
import os

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def ins():
     data = request.form['keyword']
     resp = make_response(json.dumps(data))
     resp.status_code = 200
     resp.headers['Access-Control-Allow-Origin'] = '*'
     return resp