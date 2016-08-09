from __future__ import print_function
import os
import sys
import sqlite3
import subprocess
import click
from flask import *
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)
app.config['DATABASE']=os.path.join(app.root_path, 'project1.db')
app.config['SECRET_KEY']='2309'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.before_request
def before_request():
	g.db = sqlite3.connect(app.config['DATABASE'])
	g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

@app.cli.command('initdb')
def init_db():
	before_request()
	with app.open_resource('schema.sql', mode='r') as f:
		g.db.cursor().executescript(f.read())
	g.db.commit()
	teardown_request(None)

@app.cli.command('addusers')
@click.option('--contest-id', type=int, prompt="Contest ID")
def addusers(contest_id):
	before_request()
	for row in g.db.execute('select username, password, team from entries'):
		exit_status = subprocess.call(['echo', '-c', 
			str(contest_id), '-p', row[1], row[0], row[2], row[0]])
		print(exit_status)
	teardown_request(None)

@babel.localeselector
def get_locale():
	return 'vi'

import project1.route
