import os
import time
from app import db, app, mail
from models import User
from flask import request
from werkzeug.utils import secure_filename
from flask_mail import Message
from threading import Thread


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_FILE_EXT = '.jpg'


def check_email_duplicates(email):
    ret = User.query.filter_by(email=email).first()
    return (False if ret is None else True)

def check_contact_duplicates(contact):
    ret = User.query.filter_by(contact_phone_1=contact).first()
    return (False if ret is None else True)


def gen_id(assembly, selected_ministries):
    """
    8-digit code
    1st digit: Assembly (1=Emmanuel, 2=Glory, 3=Hope)
    2nd - 6th: Position of registration
    7th - 8th: Ministries
    """
    assemblies = ["EEA", "GA", "HA"]
    ministries = ["CM", "EM", "PM", "WM", "YM"]
    valid_ministries = ['C', 'E', 'EP', 'EPY', 'EW', 'EWY', 'EY', 'P', 'PY', 'W', 'WY', 'Y']
    # get the first digit of the member id
    # EEA=1, GA=2, HA=3
    digit_1 = str(assemblies.index(assembly) + 1)
    # get the 2nd to 6th digits
    num_of_assembly_members = User.query.filter_by(assembly=assembly).count()
    digits_2_to_6 = to_given_length(num_of_assembly_members + 1, 5)
    # get the 7th and 8th digits
    selected_ministries = [m[0] for m in selected_ministries]
    selected_ministries = "".join(sorted(selected_ministries))
    if not valid_ministries.__contains__(selected_ministries):
        return ""
    digits_7_to_8 = to_given_length(valid_ministries.index(selected_ministries) + 1, 2)
    # return member id
    return (digit_1 + digits_2_to_6 + digits_7_to_8)


def to_given_length(val, length):
    """
    Returns string of a specified length (self.max_mininstry_code_len) for the value passed in
    """
    val = str(val)
    if len(val) > length:
        raise ValueError(f'Unacceptable value: Value must have length of > 0 and <= {length}')
    if len(val) == length:
        return val
    return ('0' * (length - len(val))) + val


def upload_photo(member_id):
    """
    Uploads an image file
    """
    # check if the post request has the file part
    img_file = request.files.get("kt_apps_contacts_add_avatar")
    if not img_file:
        return False
    # if user does not select file, browser also
    # submit an empty part without filename
    if img_file.filename == '':
        return False
    if img_file and allowed_file(img_file.filename):
        # remove existing src and result images
        remove_existing_img(member_id)
        # get secure filename
        filename = secure_filename(img_file.filename)
        # create unique src image name
        img_name = member_id + "_" + get_timestamp() + IMG_FILE_EXT
        # save the source image
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
        return True
    # return the index page if the form is not submitted rightly
    return False
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_timestamp():
    """
    Returns a timestamp for naming the images
    """
    timestamp = time.localtime()
    timestamp = '_'.join((str(timestamp.tm_year), str(timestamp.tm_mon), str(
        timestamp.tm_mday), str(timestamp.tm_hour), str(timestamp.tm_min), str(timestamp.tm_sec)))
    return timestamp


def remove_existing_img(member_id):
    """
    Removes an already existing image
    """
    imgs = os.listdir(app.config['UPLOAD_FOLDER'])
    for name in imgs:
        if name.startswith(member_id):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
            break


def async_send_mail(msg):

    with app.app_context():
        mail.send(msg)

def compose_email_msg(member_id, password):
    return f'<p>MEMBER ID: {member_id}\nPASSWORD: {password}</p>'

def send_email(subject, recipient, msg_content):
    msg = Message(subject, recipients=[recipient])
    msg.html = msg_content
    t = Thread(target=async_send_mail, args=[msg])
    t.start()
    return t
