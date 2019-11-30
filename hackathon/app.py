from flask import *
from templates import *
import sqlite3
import os
import shutil
import tempfile
from helper import * 
import hashlib

app = Flask(__name__)
 
app.config.from_envvar('HACKATHON_SETTINGS', silent=True)

app.config["APPLICATION_ROOT"] = '/'

app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'hackathon/var', 'uploads'
)

app.config["DATABASE_FILENAME"] = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'hackathon/var', 'hackathon.sqlite3'
)

def dict_factory(cursor, row):
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE_FILENAME'])
        g.sqlite_db.row_factory = dict_factory
        g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return g.sqlite_db


def sha256sum(filename):
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def move_upload(request_files):
    dummy, temp_filename = tempfile.mkstemp()
    file = request_files["file"]
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    dummy, suffix = os.path.splitext(file.filename)
    hash_filename_basename = hash_txt + suffix
    hash_filename = os.path.join(
        app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, hash_filename)

    return hash_filename  


def create_new_txt_file(request_files):
    new_pdf_file = move_upload(request_files)

    text = convert_pdf_to_txt(new_pdf_file)
    file_name = new_pdf_file.split('/')[-1].split('.pdf')[0]
    out_file_name = file_name + '.txt'

    out = open(os.path.join(app.config["UPLOAD_FOLDER"], out_file_name), 'w')
    out.write(text)
    out.close()

    return out_file_name

@app.route('/', methods = ['POST', 'GET'])
def show_index():
    context = {}
    return render_template("login.html", **context)


@app.route('/login', methods = ['POST', 'GET'])
def show_login():
    context = {}
    return render_template("login.html", **context)

@app.route('/home', methods = ['POST', 'GET'])
def show_home():
    cursor = get_db()

    if request.method == 'POST':
        if 'upload' in request.form and 'file' in request.files and ".pdf" in request.files["file"].filename:
            new_txt_file = create_new_txt_file(request.files)

            fileid = 1 + cursor.execute(
                "SELECT MAX(fileid) AS maxid FROM files").fetchone()['maxid']

            topic = request.form['topic']
            if topic == '':
                topic = "NO TOPIC"
            cursor.execute(
                "INSERT INTO files(fileid, filename, unitid, topic) "
                "VALUES('{}', '{}', 'null', '{}')".format(fileid, new_txt_file, topic))

            return redirect(url_for('show_quiz', files=[new_txt_file]))

        if 'search' in request.form and request.form['key'] != '':
            print(request.form)
            return redirect(url_for('show_search', key=request.form['key']))

        if 'unit' in request.form:
            list_of_dicts = cursor.execute(
                "SELECT filename FROM files WHERE unitid='{}'".format(request.form['unitid'])
                ).fetchall()
            files = []
            for item in list_of_dicts:
                files.append(list_of_dicts['filename'])
            return redirect(url_for('show_quiz', files=files))


    context = {}
    context['units'] = cursor.execute("SELECT * FROM units").fetchall()
    return render_template("home.html", **context)


@app.route('/quiz/<files>', methods = ['POST', 'GET'])
def show_quiz(files):
    # generate quiz from files
    context = {}
    return render_template("quiz.html", **context)

@app.route('/search/<key>', methods = ['POST', 'GET'])
def show_search(key):
    cursor = get_db()

    files = cursor.execute("SELECT filename, topic, unitid FROM files").fetchall()
    filtered_files = []
    for file in files:
        if search(key, os.path.join(app.config["UPLOAD_FOLDER"], file['filename'])):
            filtered_files.append(file)

    context = {}
    context['key'] = key
    if len(filtered_files) == 0:
        context['units'] = []
        return render_template("search.html", **context)
    else:
        unit = {}
        unit['unitid'] = filtered_files[0]['unitid']
        prev = filtered_files[0]['unitid']
        unit['files'] = [filtered_files[0]]
        context['units'] = [unit]
        for i in range(1, len(filtered_files)):
            if filtered_files[i]['unitid'] == prev:
                unit['files'].append(filtered_files[i])
            else:
                unit = {}
                unit['unitid'] = filtered_files[i]['unitid']
                prev = filtered_files[i]['unitid']
                unit['files'] = [filtered_files[i]]
                context['units'].append(unit)
        
    print(context)
    return render_template("search.html", **context)

@app.route('/file/<file>', methods = ['POST', 'GET'])
def show_file(file):
    cursor = get_db()
    context = {}
    file_read = open(os.path.join(app.config["UPLOAD_FOLDER"], file), 'r')
    context['text'] = []
    for line in file_read:
        context['text'].append(line)
    topic = cursor.execute("SELECT topic FROM files WHERE filename='{}'".format(file)).fetchone()['topic']
    context['topic'] = topic
    file_read.close()
    return render_template("file.html", **context)
