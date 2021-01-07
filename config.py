import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # GENERAL CONFIGURATIONS
    SECRET_KEY = b'On\xab\xf6j\nA\xe6cB.4\x97\x0e\xdb\x15'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # DO NOT CACHE
    SEND_FILE_MAX_AGE_DEFAULT = 0
    
    # DATABASE CONFIGURATIONS
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or ('sqlite:///' + os.path.join(base_dir, 'app.db'))
    # dialect+driver://username:password@host:port/database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:@127.0.0.1:3306/copkad'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://copkad_admin:copkad_admin@www.db4free.net:3306/copkad'
    UPLOAD_FOLDER = 'static' + os.sep + 'storage'

    # EMAIL CONFIGURATIONS
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SENDER_NAME = 'COP-Nsema'
    MAIL_USERNAME = 'copkad@yahoo.com'
    MAIL_DEFAULT_SENDER = 'copkad@yahoo.com'
    MAIL_PASSWORD = 'oohcikgdptuhpdfy'

    # SMS API key
    SMS_API_KEY = 'wYlETdU1fcrjy4Ql0nHESio4c'
    SMS_SENDER_ID = 'COP-Nsema'
