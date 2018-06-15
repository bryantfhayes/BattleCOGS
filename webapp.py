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

def get_matches():
    matches = []
    for filename in os.listdir("matches"):
        if filename.endswith(".match"): 
            matches.append(os.path.join("matches", filename))
    return matches

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    return _upload(request)

@app.route('/upload', methods=['POST'])
def upload_file():
    return _upload(request)

@app.route('/play', methods=['POST'])
def play():
    if 'match' not in request.form:
        return "MISSING MATCH FILE", 400

    match = request.form["match"]

    return Response(render_template('playback.html', match=match, mimetype='text/html'))

#
# Show main home page, where users can access submission forms 
#
@app.route('/', methods=['GET'])
def index():
    matches = get_matches()
    return Response(render_template('index.html', matches=matches, mimetype='text/html'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")