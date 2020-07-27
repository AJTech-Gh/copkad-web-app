from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db

class User(db.Model):
    # personal info page
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.String(30), nullable=False)
    order_id = db.Column(db.String(20), primary_key=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False, index=True)
    lastname = db.Column(db.String(50), unique=False, nullable=False, index=True) 
    othernames = db.Column(db.String(50), unique=False, nullable=False, index=True) 
    gender = db.Column(db.String(1), unique=False, nullable=False) 
    occupation = db.Column(db.String(50), unique=False, nullable=False) 
    contact_one = db.Column(db.String(14), unique=False, nullable=False, index=True) 
    contact_two = db.Column(db.String(14), unique=False, nullable=False, index=True) 
    dob = db.Column(db.DateTime(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    marital_status = db.Column(db.String(10), unique=False, nullable=False)
    area = db.Column(db.String(50), unique=False, nullable=False)
    district = db.Column(db.String(50), unique=False, nullable=False)
    church_affiliation = db.Column(db.String(50), unique=False, nullable=False)
    
    # Account seettings page
    dashboard_link = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    mode_of_communication = db.Column(db.String(6), unique=False, nullable=False)
    
    # Address Details
    address_line_one = db.Column(db.String(100), unique=False, nullable=False)
    address_line_two = db.Column(db.String(100), unique=False, nullable=False)
    digital_address = db.Column(db.String(15), unique=False, nullable=False)
    region = db.Column(db.String(30), unique=False, nullable=False)
    district = db.Column(db.String(50), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User: {self.order_id} - {self.lastname}, {self.first_name} {self.othername}'