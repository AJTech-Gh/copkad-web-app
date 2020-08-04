import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # GENERAL CONFIGURATIONS
    SECRET_KEY = b'On\xab\xf6j\nA\xe6cB.4\x97\x0e\xdb\x15'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # DATABASE CONFIGURATIONS
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ('sqlite:///' + os.path.join(base_dir, 'app.db'))
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:@127.0.0.1:3306/copkad'
    UPLOAD_FOLDER = 'static'

    # EMAIL CONFIGURATIONS
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'unibasesoftware@gmail.com'
    MAIL_DEFAULT_SENDER = 'unibasesoftware@gmail.com'
    MAIL_PASSWORD = 'Godisgood2018'
