import os, sys
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__,template_folder=’templates’)
#functions to be added here for
#different actions

if __name__ == ’__main__’:
# Run the Flask app
app.run(host=’127.0.0.1’,debug=True,port=5000)

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
		conn = psycopg2.connect(database = "mydb", user = "myuser", \
		password = "mypass", host = "127.0.0.1", port = "5432") # connect to the PostgreSQL database
		cur = conn.cursor() # create a new cursor
		cur.execute("INSERT INTO Candidate (cno, name, email) \
		VALUES (%s, %s, %s)", (cno, name, email)) # execute the INSERT statement
		conn.commit() # commit the changes to the database
		cur.close() # close the cursor
	except (Exception, psycopg2.DatabaseError) as error:
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
		conn = psycopg2.connect(database = "mydb", user = "myuser", \
		password = "mypass", host = "127.0.0.1", port = "5432")
		cur = conn.cursor() # create a new cursor
		# execute the SELECT statement
		cur.execute("SELECT cno, name, email FROM Candidate")
		results = cur.fetchall() # fetches all rows of the query result set
		cur.close() # close the cursor
	except (Exception, psycopg2.DatabaseError) as error:
		render_template("fail.html")
	finally:
		conn.close() # close the connection
	return render_template("viewall.html",rows = results)
