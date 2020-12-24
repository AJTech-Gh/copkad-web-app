from enum import unique
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import app, db, login_manager
import re

class User(UserMixin, db.Model):
    # personal info page
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(30), primary_key=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False, index=True)
    last_name = db.Column(db.String(50), unique=False, nullable=False, index=True) 
    other_names = db.Column(db.String(50), unique=False, nullable=False, index=True)
    gender = db.Column(db.String(6), unique=False, nullable=False)
    occupation = db.Column(db.String(50), unique=False, nullable=False)
    contact_phone_1 = db.Column(db.String(14), unique=False, nullable=False, index=True)
    contact_phone_2 = db.Column(db.String(14), unique=False, nullable=False, index=True)
    dob = db.Column(db.DateTime(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    marital_status = db.Column(db.String(10), unique=False, nullable=False)
    assembly = db.Column(db.String(30), unique=False, nullable=False)
    ministry = db.Column(db.String(50), unique=False, nullable=True)
    group = db.Column(db.String(50), unique=False, nullable=True)
    # Account settings page
    #dashboard_link = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    comm_email = db.Column(db.Integer, unique=False, nullable=False)
    comm_sms = db.Column(db.Integer, unique=False, nullable=False)
    comm_phone = db.Column(db.Integer, unique=False, nullable=False)
    # Address Details
    address_line_1 = db.Column(db.String(100), unique=False, nullable=False)
    address_line_2 = db.Column(db.String(100), unique=False, nullable=False)
    digital_address_code = db.Column(db.String(15), unique=False, nullable=False)
    region = db.Column(db.String(30), unique=False, nullable=False)
    district = db.Column(db.String(50), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    # relationships
    # baptism = db.relationship('Baptism', backref='user', lazy=True)
    # attendance = db.relationship('Attendance', backref='user', lazy=True)

#https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def set_contact_phone_1(self, contact):
        self.contact_phone_1 = re.sub(r"[\+\-\s]+", "", contact)

    def set_contact_phone_2(self, contact):
        self.contact_phone_2 = re.sub(r"[\+\-\s]+", "", contact)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_dob(self, dob):
        dob = dob.split('-')
        self.dob = datetime(int(dob[0]), int(dob[1]), int(dob[2]))

    def get_dob(self, dob):
        return '{}-{}-{}'.format(dob.year, dob.month, dob.day)

    def set_ministry(self, ministry):
        self.ministry = ",".join(ministry)

    def set_group(self, group):
        self.group = ("" if not group else group)

    def set_comm_email(self, comm_email):
        self.comm_email = (1 if comm_email and comm_email.lower() == 'on' else 0)

    def get_comm_email(self, comm_email):
        return ('on' if comm_email == 1 else 'off')

    def set_comm_sms(self, comm_sms):
        self.comm_sms = (1 if comm_sms and comm_sms.lower() == 'on' else 0)

    def get_comm_sms(self, comm_sms):
        return ('on' if comm_sms == 1 else 'off')

    def set_comm_phone(self, comm_phone):
        self.comm_phone = (1 if comm_phone and comm_phone.lower() == 'on' else 0)

    def get_comm_phone(self, comm_phone):
        return ('on' if comm_phone == 1 else 'off')

    def __repr__(self):
        return f'User: {self.member_id} - {self.last_name}, {self.first_name} {self.other_names}'

class Transfer(db.Model):
    #Transfered member info
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    #Transfer records
    transfered_from = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    transfered_to = db.Column(db.String(50), unique=False, nullable=False)
    present_portfolio = db.Column(db.String(50), unique=False, nullable=False)
    transfer_specification = db.Column(db.String(100), unique=False, nullable=False)
    transfer_date = db.Column(db.DateTime(), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)

    def set_transfer_date(self, transfer_date):
        _date, _time = transfer_date.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.transfer_date = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def get_promotion_date(self, transfer_date):
        return '{}-{}-{} {}:{}'.format(transfer_date.year, transfer_date.month, transfer_date.day, transfer_date.hour, transfer_date.minute)

    def __repr__(self):
        return f'User: {self.member_id}'

class Promotion(db.Model):
    #Promoted member info
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    #Promotion records
    present_portfolio = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    promoted_portfolio = db.Column(db.String(50), unique=False, nullable=False)
    portfolio_specification = db.Column(db.String(80), unique=False, nullable=False)
    promotion_date = db.Column(db.DateTime(), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)

    def set_promotion_date(self, promotion_date):
        _date, _time = promotion_date.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.promotion_date = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def get_promotion_date(self, promotion_date):
        return '{}-{}-{} {}:{}'.format(promotion_date.year, promotion_date.month, promotion_date.day, promotion_date.hour, promotion_date.minute)

    def __repr__(self):
        return f'User: {self.member_id}'

class Birth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id_father = db.Column(db.String(20), nullable=False, index=True)
    member_id_mother = db.Column(db.String(20), nullable=False, index=True)
    child_name = db.Column(db.String(50), unique=False, nullable=False, index=True)
    child_dob = db.Column(db.DateTime(), unique=False, nullable=False)
    ceremony_date_time = db.Column(db.DateTime(), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)
    assembly = db.Column(db.String(30), unique=False, nullable=False)

    def set_child_dob(self, child_dob):
        child_dob = child_dob.split('-')
        self.child_dob = datetime(int(child_dob[0]), int(child_dob[1]), int(child_dob[2]))

    def get_child_dob(self, child_dob):
        return '{}-{}-{}'.format(child_dob.year, child_dob.month, child_dob.day)

    def set_ceremony_date_time(self, ceremony_date_time):
        _date, _time = ceremony_date_time.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.ceremony_date_time = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def get_ceremony_date_time(self, ceremony_date_time):
        return '{}-{}-{} {}:{}'.format(ceremony_date_time.year, ceremony_date_time.month, ceremony_date_time.day, ceremony_date_time.hour, ceremony_date_time.minute)

    def __repr__(self):
        return f'Name: {self.child_name}\nDate of Birth: {self.child_dob}'

class Death(db.Model):
    #Deceased member info
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    #Death records
    death_date = db.Column(db.DateTime(), unique=False, nullable=False)
    burial_date = db.Column(db.DateTime(), unique=False, nullable=False)
    place_of_burial = db.Column(db.String(50), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)

    def set_death_date(self, death_date):
        death_date = death_date.split('-')
        self.death_date = datetime(int(death_date[0]), int(death_date[1]), int(death_date[2]))

    def get_death_date(self, death_date):
        return '{}-{}-{}'.format(death_date.year, death_date.month, death_date.day)

    def set_burial_date(self, burial_date):
        burial_date = burial_date.split('-')
        self.burial_date = datetime(int(burial_date[0]), int(burial_date[1]), int(burial_date[2]))

    def get_burial_date(self, burial_date):
        return '{}-{}-{}'.format(burial_date.year, burial_date.month, burial_date.day)

    def __repr__(self):
        return f'User: {self.member_id}'

class Baptism(db.Model):
    # account info
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    # baptism records
    date_of_baptism = db.Column(db.DateTime(), unique=False, nullable=False)
    place_of_baptism = db.Column(db.String(50), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)
    district = db.Column(db.String(50), unique=False, nullable=False)
    area = db.Column(db.String(50), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)


    def set_date_of_baptism(self, date_of_baptism):
        date_of_baptism = date_of_baptism.split('-')
        self.date_of_baptism = datetime(int(date_of_baptism[0]), int(date_of_baptism[1]), int(date_of_baptism[2]))

    def get_date_of_baptism(self, date_of_baptism):
        return '{}-{}-{}'.format(date_of_baptism.year, date_of_baptism.month, date_of_baptism.day)

    def __repr__(self):
        return f'User: {self.member_id}'


class RalliesAndConventions(db.Model):
    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cr_type = db.Column(db.String(30), unique=False, nullable=False)
    cr_title = db.Column(db.String(100), unique=False, nullable=False)
    start_date_time = db.Column(db.DateTime(), unique=False, nullable=False)
    end_date_time = db.Column(db.DateTime(), unique=False, nullable=False)
    assembly = db.Column(db.String(30), unique=False, nullable=False)
    venue = db.Column(db.String(50), unique=False, nullable=False)
    souls_won = db.Column(db.Integer, unique=False, nullable=False)
    head_count = db.Column(db.Integer, unique=False, nullable=False)
    mode_of_count = db.Column(db.String(30), unique=False, nullable=False)


    def set_start_date_time(self, start_date_time):
        _date, _time = start_date_time.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.start_date_time = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def set_end_date_time(self, end_date_time):
        _date, _time = end_date_time.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.end_date_time = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def get_start_date_time(self, start_date_time):
        return '{}-{}-{} {}:{}'.format(start_date_time.year, start_date_time.month, start_date_time.day, start_date_time.hour, start_date_time.minute)

    def get_end_date_time(self, end_date_time):
        return '{}-{}-{} {}:{}'.format(end_date_time.year, end_date_time.month, end_date_time.day, end_date_time.hour, end_date_time.minute)

    def __repr__(self):
        return f'cr_id: {self.cr_id} \nFrom: {self.get_start_date_time(self.start_date_time)} \nTo: {self.get_end_date_time(self.end_date_time)}'


class Dedication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id_father = db.Column(db.String(20), nullable=False, index=True)
    member_id_mother = db.Column(db.String(20), nullable=False, index=True)
    child_name = db.Column(db.String(50), unique=False, nullable=False, index=True)
    child_dob = db.Column(db.DateTime(), unique=False, nullable=False)
    dedication_date_time = db.Column(db.DateTime(), unique=False, nullable=False)
    officiating_minister = db.Column(db.String(50), unique=False, nullable=False)
    assembly = db.Column(db.String(30), unique=False, nullable=False)
    place_of_ceremony = db.Column(db.String(50), unique=False, nullable=False)


    def set_child_dob(self, child_dob):
        child_dob = child_dob.split('-')
        self.child_dob = datetime(int(child_dob[0]), int(child_dob[1]), int(child_dob[2]))

    def get_child_dob(self, child_dob):
        return '{}-{}-{}'.format(child_dob.year, child_dob.month, child_dob.day)

    def set_dedication_date_time(self, dedication_date_time):
        _date, _time = dedication_date_time.split()
        _date = _date.split('-')
        _time = _time.split(':')
        self.dedication_date_time = datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))

    def get_dedication_date_time(self, dedication_date_time):
        return '{}-{}-{} {}:{}'.format(dedication_date_time.year, dedication_date_time.month, dedication_date_time.day, dedication_date_time.hour, dedication_date_time.minute)

    def __repr__(self):
        return f'Name: {self.child_name}\nDate of Birth: {self.child_dob}'


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    event = db.Column(db.String(50), unique=False, nullable=False, index=True)
    date = db.Column(db.DateTime(), unique=False, nullable=False)
    status = db.Column(db.String(1), unique=False, nullable=False, index=True)
    time_in = db.Column(db.String(6), unique=False, nullable=False, index=True)
    time_out = db.Column(db.String(6), unique=False, nullable=False, index=True)

    def set_date(self, date):
        date = date.split('-')
        self.date = datetime(int(date[2]), int(date[1]), int(date[0]))

    def get_date(self, date):
        return '{}-{}-{}'.format(date.year, date.month, date.day)


class Accessibility(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.String(20), db.ForeignKey('user.member_id'), nullable=False, index=True)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    permission = db.Column(db.String(50), unique=False, nullable=False, index=True)
    assembly = db.Column(db.String(30), unique=False, nullable=False)
    assembly_status = db.Column(db.String(10), unique=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Accessibility: {self.member_id}\nPermission: {self.permission}'


@login_manager.user_loader
def load_user(id):
    return Accessibility.query.get(int(id))