import os, sys
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='templates')
#functions to be added here for
#different actions

if __name__ == '__main__':
# Run the Flask app
  app.run(host='0.0.0.0',debug=True,port=5000)

@app.route("/")
def index():
	return render_template("index.html");

@app.route("/add")
def add():
	return render_template("add.html")

@app.route("/savedetails",methods = ["POST"])
def saveDetails():
	cno = request.form["cno"]
	name = request.form["name"]
	email = request.form["email"]
	conn = None
	try:
		conn = sqlite3.connect('example.db') # connect to the PostgreSQL database
		cur = conn.cursor() # create a new cursor
		cur.execute("INSERT INTO Candidate (cno, name, email) \
		VALUES (%s, %s, %s)", (cno, name, email)) # execute the INSERT statement
		conn.commit() # commit the changes to the database
		cur.close() # close the cursor
	except (Exception, sqlite3.DatabaseError) as error:
		render_template("fail.html")
	finally:
		if conn is not None:
		  conn.close() # close the connection
	return render_template("success.html")

@app.route("/viewall")
def viewAll():
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = sqlite3.connect('example.db')
		cur = conn.cursor() # create a new cursor
		# execute the SELECT statement
		cur.execute("SELECT cno, name, email FROM Candidate")
		results = cur.fetchall() # fetches all rows of the query result set
		cur.close() # close the cursor
	except (Exception, sqlite3.DatabaseError) as error:
		render_template("fail.html")
	finally:
		conn.close() # close the connection
	return render_template("viewall.html",rows = results)
