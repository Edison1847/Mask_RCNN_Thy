import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
import sys
from werkzeug.utils import secure_filename
# from demo2 import execute
from demo2 import execute
import cv2
import numpy as np
import codecs, json
import time

# Root directory of the project
ROOT_DIR = os.path.abspath("../")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library

UPLOAD_FOLDER = '../images/'
PREDICTED_IMAGES = "./uploads/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
noClass = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDICTED_FOLDER'] = PREDICTED_IMAGES

@app.route("/")
def home():
    return render_template("index.html")
def move_forward():
    #Moving forward code
    print("Moving Forward...")
    return render_template('about.html', message=forward_message);



@app.route('/show/<filename>', methods=['GET', 'POST'])
def show(filename):

    # file =request.files['file']
    # print(file.filename)
    # image = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/uploads/" + filename)
    # image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # print(image)
    return render_template("show.html")

@app.route('/getImage3/<filename>', methods=['GET', 'POST'])
def getImage3(filename):

    IMPORT_DIR = os.path.join(ROOT_DIR, "images/")  # To find local version

    # file =request.files['file']
    # print(file.filename)
    # image = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/uploads/" + filename)
    # image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # print(image)

    # filename = "Masked_Image.jpg"
    filename = filename
    print(filename)
    print(IMPORT_DIR)
    # return send_from_directory(app.config['PREDICTED_FOLDER'], filename)
    # return(filename)
    # return ""
    return send_from_directory(IMPORT_DIR, filename)

@app.route('/getMaskedImage/')
def getMaskedImage():
    filename = "Masked_Image.png"
    return send_from_directory("uploads", filename)

@app.route('/analyzedImage', methods=['GET', 'POST'])
def analyzedImage():
    print("inside analyze")
    filename = "1.jpg"
    out = execute(filename)
    # print (out)

    filename = "Masked_Image.jpg"
    print(out)
    # time.sleep(5)
    return out
    # return masked_image
    # print(send_from_directory("uploads", masked_image)
    # return send_from_directory("uploads", masked_image)



@app.route('/showAnalyzedImage/')
def showAnalyzedImage():
    filename = "Masked_Image.jpg"
    # return send_from_directory("uploads", filename)
    print("Show analyzed images")
    return render_template("analyzed.html")

@app.route('/generateAnalyzedImage', methods=['GET', 'POST'])
def generateAnalyzedImage():
    filename = "Masked_Image.jpg"
    # return send_from_directory("uploads", filename)
    print("inside image")
    return send_from_directory(app.config['PREDICTED_FOLDER'], filename)


@app.route('/downloadFile', methods=['GET', 'POST'])
def downloadFile():
    filename = "Masked_Image.jpg"
    try:
        path = os.path.join(app.config['PREDICTED_FOLDER'], filename)
        print(path)
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)






@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = "1.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved")

    return redirect(url_for('show', filename=filename))


    # return render_template("upload.html")


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
