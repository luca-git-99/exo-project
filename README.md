# exo-project

''' webapp to upload a RAW image to a folder and convert it to JPEG,
The index.html page shows the upload form and thumbnail of the files processed.
A md5 and sha1 checsum is shows with the file name for further processing.

ie  RAW_CANON_S30.CRW >>> /uploads/RAW_CANON_S30.CRW.jpg?SHA1=SHA1%3A+8b02b7a508a1b338a3ee24f02007d83373a4e252"

do@do:~/$ python3 app4.py 
 * Serving Flask app 'app4'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
Open browser on http://127.0.0.1:5000

live demo: https://palucaville.pythonanywhere.com/


