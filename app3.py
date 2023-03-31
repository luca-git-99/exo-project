''' webapp to upload a RAW image to a folder and convert it to JPEG,
The index.html page shows the upload form and Thumbnail of the files processed.
the name of the new jpg image is the same as the RW + a timestamp.
'''
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import rawpy
import imageio
import os

from datetime import datetime
datestamp = datetime.now().date()

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.crw','.cr2','.nef']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    ## some file check
    if filename != '':
        file_ext = (os.path.splitext(filename)[1]).lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        ## file is saved, do the conversion
        convert(os.path.join(app.config['UPLOAD_PATH'], filename), filename)
    return redirect(url_for('index'))

def convert(raw_in, fname):
    raw = rawpy.imread(raw_in)
    rgb = raw.postprocess()
    imageio.imsave(os.path.join(app.config['UPLOAD_PATH'], f'{fname} {datestamp}.jpg'), rgb)
 

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == "__main__":
    app.run(debug = True)
