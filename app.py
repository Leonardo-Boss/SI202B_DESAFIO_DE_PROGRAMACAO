import time
import pickle
import os

from flask import Flask, render_template, request
import webview

from moodle_api import Moodle

app = Flask(__name__)

@app.route('/')
def index():
    if os.path.exists('temp'):
        with open('temp', 'rb') as file:
            form = pickle.load(file)
        moodle = Moodle(form[0], form[1])
        events = moodle.get_events()[0]['data']['events']
        return render_template('painel.html', events=events, time=time)
    return render_template('login.html')

@app.route('/painel', methods=['POST'])
def login():
    if request.form['remember'] == 'true':
        form = [request.form['username'], request.form['password']]
        with open('temp', 'wb') as file:
            pickle.dump(form, file)
    moodle = Moodle(request.form['username'], request.form['password'])
    events = moodle.get_events()[0]['data']['events']
    return render_template('painel.html', events=events, time=time)

@app.route('/logout', methods=['POST'])
def logout():
    if os.path.exists('temp'):
        os.remove('temp')
    return render_template('login.html')


if __name__ == '__main__':
    webview.create_window('moodle', app)
    webview.start()