import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = b'On\xab\xf6j\nA\xe6cB.4\x97\x0e\xdb\x15'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ('sqlite:///' + os.path.join(base_dir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True