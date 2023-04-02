''' webapp to upload a RAW image to a folder and convert it to PNG,
The index.html page shows the upload form and Thumbnail of the files processed.

'''
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime
import rawpy
import imageio
import os


datestamp = datetime.now().date()
watermark = "watermark.png" # watermark image


app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.crw','.cr2','.nef'] # case NON sensitive
app.config['UPLOAD_PATH'] = 'uploads'
app.config['TESTING'] = True
app.config['DEBUG'] = True

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    png_files = []    
    for afile in files:
        if afile.endswith('.png'): 
            png_files.append(afile)
    return render_template('index.html', files=png_files)

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
        convertRaw(os.path.join(app.config['UPLOAD_PATH'], filename), filename)
    return redirect(url_for('index'))

def convertRaw(raw_in, fname):
    raw = rawpy.imread(raw_in)
    rgb = raw.postprocess()
    #imageio.imsave(os.path.join(app.config['UPLOAD_PATH'], f'{fname} {datestamp}.png'), rgb)
    imageio.imsave(os.path.join(app.config['UPLOAD_PATH'], f'{fname}.png'), rgb) 
     
    # watermark SETTINGS
    source = (os.path.join(app.config['UPLOAD_PATH'], f'{fname}.png')) # source image
    target = (os.path.join(app.config['UPLOAD_PATH'], f'{fname}.png')) # destination image (same as source)
    watermark = "watermark.png" # watermark image
     
    # DRAW WATERMARK & SAVE
    imgS = Image.open(source).convert("RGBA")
    imgW = Image.open(watermark)
    imgS.paste(imgW, (10,10), imgW.convert("RGBA"))
    imgS.save(target, format="png", quality=95)
    
@app.route('/uploads/<filename>') ## serves a page with the new converted file
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == "__main__":
    app.run(debug = True)
