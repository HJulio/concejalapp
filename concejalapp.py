__author__ = 'hjulio'
# -*- coding: utf-8 -*-

import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


app = Flask(__name__)


ETA_words = ['ETA', 'eta', 'matar', 'Cifuentes', 'judio', 'Israel', 'bomba', 'bombas', 'Aguirre', 'Podemos']


ETA_tweets = []

# Allowed
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])


def process(file):

    ETA_dic = {}
    reader = csv.reader(file)
    for row in reader:
        for word in row[5].split():
            if word in ETA_words:
                ETA_dic[row[0]] = row[5]
                print (row[0] + "," + row[5]) #debug
                break;
    return ETA_dic


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        d=process(file)
        return render_template('tweets.html', ETA_dic=d)

    else:
        return redirect(url_for('error'))


# If error (wrong extension / empty)
@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.debug = True
    app.run(
        host="localhost"
    )
