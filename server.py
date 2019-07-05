from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import sqlite3

app = Flask(__name__)
dropzone = Dropzone(app)
############################################################
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB
##############################################################


# location D:\Downloads\sqlite-tools-win32-x86-3280000\sqlite-tools-win32-x86-3280000\coord.db

@app.route('/show')
def show():
	conn = sqlite3.connect("coord.db")
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
		conn = sqlite3.connect("coord.db")
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
		conn = sqlite3.connect("coord.db")
		crsr = conn.cursor()
		crsr.execute("SELECT * FROM COORDS")
		ans = crsr.fetchall()
		conn.close()
		res = ""
		for row in ans:
			if row[2]!=None:
				res+=str(row[2])+" "
		return res

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    # handle image upload from Dropszone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )

            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')


@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

