



from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from flask import jsonify
from werkzeug.utils import secure_filename
#from PIL import Image
import cv2 #  pip install opencv-python
from datetime import datetime
import rawpy
import imageio
import os
import hashlib
from ipstack import GeoLookup

# Create the GeoLookup object using your API key.
geo_lookup = GeoLookup("2116cdb68c02bea453abbb0d222bb6a2")





#datestamp = datetime.now().date()
#posix_time = datetime.now().timestamp()

UPLOAD_FOLDER = 'static/uploads' # becomes app.config['UPLOAD_PATH']
ALLOWED_JPG_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BUF_SIZE = 65536  #  64kb chunks buffer for hashing!



app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_RAW_EXTENSIONS'] = ['.crw','.cr2','.nef'] # case NON sensitive
app.secret_key = "secret key"
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER 
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    location = geo_lookup.get_own_location()
    #print(location)
    return (location), 200

@app.route('/sketcher')
def sketcher():
    return render_template('sketcher.html')

def allowed_jpg_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_JPG_EXTENSIONS

@app.route('/sketcher',methods=['POST'])
def sketch():
    file = request.files['file']
    if file and allowed_jpg_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        sketch_img = make_sketch(img)
        sketch_img_name = filename.split('.')[0]+"_sketch.jpg"
        _ = cv2.imwrite(UPLOAD_FOLDER+'/'+sketch_img_name, sketch_img)
        return render_template('sketcher.html',org_img_name=filename,sketch_img_name=sketch_img_name)

def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result

def delete_uploads():
    files_to_del = os.listdir(app.config['UPLOAD_PATH'])
    for file_d in files_to_del:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file_d))
    

    

def hash_file(raw_in):
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()
    with open(raw_in, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
            md5.update(data)
    md5_text = ("MD5: {0}".format(md5.hexdigest()))
    sha_text = ("SHA1: {0}".format(sha1.hexdigest()))
    return sha_text, md5_text


def allowed_raw_file(filename):
    allowed_raw = app.config['UPLOAD_RAW_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_raw

@app.route('/converter')
def converter():
  return render_template('converter.html')

@app.route('/converter', methods=['POST'])
def convert_files():
    file = request.files['file']
    #if file and allowed_raw_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    raw_input = os.path.join(app.config['UPLOAD_PATH'], filename)
    datestamp = datetime.now().isoformat()
    raw = rawpy.imread(raw_input)
    rgb = raw.postprocess()
    imageio.imsave(os.path.join(app.config['UPLOAD_PATH'], f'{filename}_{datestamp}.jpg'), rgb)
    jpg_out = os.path.join(app.config['UPLOAD_PATH'], f'{filename}_{datestamp}.jpg')
    return render_template('converter.html', r_out=jpg_out)

@app.route('/static/uploads/<filename>') ## serves a page with the new converted file
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ... This route will always give a 500 Internal Server Error regardless of whether the debugger is running or not:
@app.route('/500')
def error500():
    abort(500)

if __name__ == "__main__":
    app.run(debug = True)
