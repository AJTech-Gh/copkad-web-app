import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = b'On\xab\xf6j\nA\xe6cB.4\x97\x0e\xdb\x15'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ('sqlite:///' + os.path.join(base_dir, 'app.db'))
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:@127.0.0.1:3306/copkad'
    SQLALCHEMY_TRACK_MODIFICATIONS = True