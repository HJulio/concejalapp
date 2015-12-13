__author__ = 'hjulio'
# -*- coding: utf-8 -*-

import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Allowed
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])


def process(file_, words):
	eta_dic = {}
	reader = csv.reader(file_)
	for row in reader:
		for word in row[5].split():
			if word in words:
				eta_dic[row[0]] = row[5]
				break
	return eta_dic


def allowed_file(filename):
	return '.' in filename and \
	       filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
	eta_words = ['ETA', 'eta', 'matar', 'etarra', 'etarras', 'Cifuentes', 'judio', 'Israel', 'bomba', 'bombas', 'Aguirre', 'Podemos', 'Venezuela']

	file_ = request.files['file']
	for w in request.form['palabrasExtra'].split(','):
		eta_words.append(w.strip(' '))

	if file_ and allowed_file(file_.filename):
		d = process(file_, eta_words)
		return render_template('tweets.html', ETA_dic=d)

	else:
		return redirect(url_for('error'))


# If error (wrong extension / empty)
@app.route('/error')
def error():
	return render_template('error.html')


if __name__ == '__main__':
	app.run(
			host="localhost"
	)
