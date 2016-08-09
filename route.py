from flask import *
from project1 import app

@app.route('/')
def home():
	config = g.db.execute('select * from config').fetchone()
	return render_template('home.html', **dict(config))

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
	return redirect(url_for('home'))
	
def table_keys(table):
	return [row['name'] for row in g.db.execute('pragma table_info({})'.format(table))]

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	config = dict(g.db.execute('select * from config').fetchone())
	if request.method=='GET':
		return render_template('edit.html', **config)
	else:
		#for key in config.keys():
		for key in table_keys('config'):
			if key in request.form:
				g.db.execute('update config set {}=?'.format(key), [request.form[key]])
		g.db.commit()
		flash("Config saved")
		return redirect(url_for('edit'))

@app.route('/reports', methods=['GET', 'POST'])
def reports():
	if request.method=='GET':
		config = dict(g.db.execute('select * from config').fetchone())
		reports = g.db.execute('select * from reports').fetchall()
		return render_template('reports.html', reports=reports, **config)
	else:
		g.db.execute('insert into reports(star, report, details) values(?, ?, ?)',
			[request.form['star'], request.form['report'], request.form['details']])
		g.db.commit()
		flash("Report successfully")
	return redirect(url_for('reports'))
