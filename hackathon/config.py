import os
import flask
app = flask.Flask(__name__)
APPLICATION_ROOT = '/'

# SECRET_KEY = b'\x18=\xf6^\xd7\xb2NG\xfb\xd1\xa1\x11\xdf\x03\xb2\xf1Z\xa0kNG\xee\x9a\xd3'
# SESSION_COOKIE_NAME = 'login'

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'hackathon.sqlite3'
)