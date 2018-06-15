import os, copy
from flask import Flask, request, redirect, url_for, render_template, Response, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

def _upload(request):
    if 'file' not in request.files or request.files['file'].filename == "":
        return "MISSING FILE", 400

    file = request.files['file']

    # If tmp doesnt exist, make it
    if not os.path.isdir("bots"):
        os.mkdir("bots")

    if file:
        filename = secure_filename(file.filename)
        if not filename.endswith(".py"):
            return "BAD FILE TYPE", 400
        file.save(os.path.join("bots", filename))
        return "OK", 200

    return "UNKNOWN ERROR", 400

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    return _upload(request)

@app.route('/upload', methods=['POST'])
def upload_file():
    return _upload(request)

#
# Show main home page, where users can access submission forms 
#
@app.route('/', methods=['GET'])
def index():
    return Response(render_template('index.html', mimetype='text/html'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")