# -*- coding: utf-8 -*

import os
from flask import Flask, render_template, request, json
from werkzeug import generate_password_hash, check_password_hash
try:
	from flask.ext.mysql import MySQL
except:
	from flask_mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations/ENV Vars
app.config['MYSQL_DATABASE_USER'] = os.environ['NANA_DB_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['NANA_DB_PASS']
app.config['MYSQL_DATABASE_DB'] = os.environ['NANA_DB_NAME']
app.config['MYSQL_DATABASE_HOST'] = os.environ['NANA_DB_HOST']
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')
	#return "Nana's Recipes - Making Chocolate Great Again!"

@app.route("/submitRecipe")
def submitRecipe():
	return render_template('add_recipe.html')

@app.route("/thanks")
def thanks():
	return render_template('thanks.html')

@app.route("/recent")
def recentRecipes():
	conn = mysql.connect()
	cursor = conn.cursor()
	query = ("select title from nanas_recipes.recipes order by id DESC limit 10;")
	cursor.execute(query)
	data = cursor.fetchall()
	return render_template('recent.html',data=data)

@app.route('/addRecipe',methods=['POST','GET'])
def addRecipe(): # read the posted values from the UI
	_title = request.form['recipeTitle']
	_description = request.form['recipeDescription']
	_contributor = request.form['recipeContributor']

	# validate the received values
	if _title and _description and _contributor:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_createRecipe',(_title,_description,_contributor))
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			#return json.dumps({'html':'<span>All fields good !!</span>'})
			main()
			return redirect(url_for('thanks'))
		else:
			return json.dumps({'error':str(data[0])})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
	app.run()