import time
import pickle
import os

import appdirs
from flask import Flask, render_template, request
import webview

from moodle_api import Moodle

app = Flask(__name__)
temp = os.path.join(appdirs.user_config_dir('moodle_tarefas', False), 'temp')


@app.route('/')
def index():
    if os.path.exists(temp):
        with open(temp, 'rb') as file:
            form = pickle.load(file)
        moodle = Moodle(form[0], form[1])
        events = moodle.get_events()[0]['data']['events']
        return render_template('painel.html', events=events, time=time)
    return render_template('login.html')

@app.route('/painel', methods=['POST'])
def login():
    if request.form['remember'] == 'true':
        form = [request.form['username'], request.form['password']]
        with open(temp, 'wb') as file:
            pickle.dump(form, file)
    moodle = Moodle(request.form['username'], request.form['password'])
    events = moodle.get_events()[0]['data']['events']
    return render_template('painel.html', events=events, time=time)

@app.route('/logout', methods=['POST'])
def logout():
    if os.path.exists(temp):
        os.remove()
    return render_template('login.html')


if __name__ == '__main__':
    webview.create_window('moodle', app)
    webview.start()