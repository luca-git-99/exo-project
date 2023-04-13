# exo-project

''' webapp to upload a RAW image to a folder and convert it to JPEG. Built with the Flask miniframework.
The index.html page shows the upload form and thumbnails of the files already processed processed.

Clicking on the thumbnal will open a new Tab with full size processed picture.


uploaded file:  RAW_CANON_S30.CRW >>>   
in the index.html:  /uploads/RAW_CANON_S30.CRW.jpg_2023-04-13T15:45:12.316642.jpg""

live demo: https://palucaville.pythonanywhere.com/
 
 to run locally:
do@do:~/$ python3 app.py 
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit

Open browser on http://127.0.0.1:5000

TODO
A md5 and sha1 checksum shown with the file name for further processing.



