from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS candidate(
   cno INT,
   name TEXT,
   email TEXT,
   primary key (cno));
""")
conn.commit()
c.close()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
	return render_template("index.html")

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
    conn = sqlite3.connect('example.db')
    cur = conn.cursor() # create a new cursor
    cur.execute("INSERT INTO Candidate (cno, name, email) VALUES (?, ?, ?)", (cno, name, email)) # execute the INSERT statement
    conn.commit() # commit the changes to the database
    cur.close() # close the cursor
    return render_template("Success.html")
  except:
    return render_template("error.html")

@app.route("/viewall")
def viewAll():
	conn = None
	# connect to the PostgreSQL database
	conn = sqlite3.connect('example.db')
	cur = conn.cursor() # create a new cursor
	# execute the SELECT statement
	cur.execute("SELECT cno, name, email FROM Candidate")
	results = cur.fetchall() # fetches all rows of the query result set
	cur.close() # close the cursor
	render_template("fail.html")
	conn.close() # close the connection
	return render_template("viewall.html", rows = results)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)