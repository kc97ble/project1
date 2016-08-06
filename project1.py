from __future__ import print_function
import os
import sys
import sqlite3
import subprocess
import click
from flask import *
from flask.ext.babel import Babel

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

@app.route('/')
def show_home_page():
	config = g.db.execute('select * from config').fetchone()
	return render_template('show_home_page.html', **dict(config))

@app.route('/register', methods=['POST'])
def register():
	username = request.form['username']
	password = request.form['password']
	team = request.form['team']
	hidden = request.form['hidden']
	
	if username=='' or password=='' or team=='':
		flash("All fields must not be empty")
	elif g.db.execute('select count(*) from entries where username=?', 
		[username]).fetchone()[0] != 0:
			flash("Username existed");
	else:
		g.db.execute('insert into entries (username, password, team, hidden) values (?, ?, ?, ?)',
			[username, password, team, hidden])
		g.db.commit()
		flash("Register successfully")
	return redirect(url_for('show_home_page'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	config = dict(g.db.execute('select * from config').fetchone())
	if request.method=='GET':
		return render_template('edit.html', **config)
	else:
		print('Hello')
		for key in config.keys():
			if key in request.form:
				g.db.execute('update config set {}=?'.format(key), [request.form[key]])
		g.db.commit()
		flash("Config saved")
		return redirect(url_for('edit'))		

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
