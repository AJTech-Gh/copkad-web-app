from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import routes, models

# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=5000, debug=True)