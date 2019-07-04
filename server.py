from flask import Flask
from flask import request
import os
import sqlite3

app = Flask(__name__)

# location D:\Downloads\sqlite-tools-win32-x86-3280000\sqlite-tools-win32-x86-3280000\coord.db

@app.route('/show')
def show():
	conn = sqlite3.connect("D:\Downloads\sqlite-tools-win32-x86-3280000\sqlite-tools-win32-x86-3280000\coord.db")
	crsr = conn.cursor()
	crsr.execute("SELECT * FROM COORDS")
	ans = crsr.fetchall()
	conn.close()
	html = "<h1>Co-ordinates : </h1>"+"\n"+"<ol>"
	for row in ans:
		if row[1]!=None:
			html += "<li><h3>Latitude : "+str(row[1])+"  Longitude : "+str(row[2])+"</h3></li>"+"\n"
	html += "</ol></body>"
	return html

@app.route('/fetchx',methods=['GET','POST'])
def fetchx():
	if request.method == 'POST':
		data = request.form.get('data')
		conn = sqlite3.connect("D:\Downloads\sqlite-tools-win32-x86-3280000\sqlite-tools-win32-x86-3280000\coord.db")
		crsr = conn.cursor()
		crsr.execute("SELECT * FROM COORDS")
		ans = crsr.fetchall()
		conn.close()
		res = ""
		for row in ans:
			if row[1]!=None:
				res+=str(row[1])+" "
		return res


@app.route('/fetchy',methods=['GET','POST'])
def fetchy():
	if request.method == 'POST':
		data = request.form.get('data')
		conn = sqlite3.connect("D:\Downloads\sqlite-tools-win32-x86-3280000\sqlite-tools-win32-x86-3280000\coord.db")
		crsr = conn.cursor()
		crsr.execute("SELECT * FROM COORDS")
		ans = crsr.fetchall()
		conn.close()
		res = ""
		for row in ans:
			if row[2]!=None:
				res+=str(row[2])+" "
		return res



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
