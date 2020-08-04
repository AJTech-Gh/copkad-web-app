import os
import time
from app import db, app, mail
from models import User
from flask import request, render_template
from werkzeug.utils import secure_filename
from flask_mail import Message
from threading import Thread
import urllib
import re
import json


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_FILE_EXT = '.jpg'
PROFILE_PHOTOS_DIR = app.config['UPLOAD_FOLDER'] + os.sep + "profile_photos"
PSEUDO_PROFILE_PHOTOS_DIR = app.config['UPLOAD_FOLDER'] + os.sep + "incomplete_reg_acc" + os.sep + "profile_photos"
PSEUDO_DATA_DIR = app.config['UPLOAD_FOLDER'] + os.sep + "incomplete_reg_acc" + os.sep + "data"


def gen_pseudo_id(first_name, last_name, contact_phone_1):
    contact_phone_1 = re.sub(r"[\s\-]", "", contact_phone_1)
    return f'{first_name}_{last_name}_{contact_phone_1[-9:]}'

def save_incomplete_reg(data_dict):
    json_data = json.dumps(data_dict)
    

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
    max_prev_count = 0
    assembly_ids = User.query.filter_by(assembly=assembly).with_entities(User.member_id).all()
    for m_id in assembly_ids:
        count_str = m_id[0][1:-2]
        count = int(count_str)
        if count > max_prev_count:
            max_prev_count = count
    digits_2_to_6 = to_given_length(max_prev_count + 1, 5)
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
        img_file.save(os.path.join(PROFILE_PHOTOS_DIR, img_name))
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
    imgs = os.listdir(PROFILE_PHOTOS_DIR)
    for name in imgs:
        if name.startswith(member_id):
            os.remove(os.path.join(PROFILE_PHOTOS_DIR, name))
            break


def async_send_mail(msg):
    with app.app_context():
        mail.send(msg)

def compose_email_msg(member_id, password):
    return render_template("msg.html", member_id=member_id, password=password)

def send_email(subject, recipient, msg_content):
    msg = Message(subject, recipients=[recipient])
    msg.html = msg_content
    t = Thread(target=async_send_mail, args=[msg])
    t.start()
    return t

def async_send_sms(msg, recipient):
    # set progress signal
    print("Sending Message ...")
    # parameters to send SMS
    base_url = "https://apps.mnotify.net/smsapi?"
    api_key = "vuWSVGpTxpTeMHPxXNuQ4iRNO"
    sender_name = "COP"
    params = {"key": api_key,"to": recipient, "msg": msg, "sender_id": sender_name}
    # prepare your url
    url = base_url + urllib.parse.urlencode(params)
    try:
        # get the response
        content = urllib.request.urlopen(url).read()   # content contains the response from mNotify
        if int(content) == 1000:    # check if message was successful
            # send success message signal
            print("Message Sent")
        else:
            print("Message Not Sent")
    except:
        # send error message signal
        print("Fatal error")

def compose_sms_msg(member_id, password):
    return f'Membership Account Details\n\nMEMBER ID: {member_id}\nPASSWORD: {password}'

def send_sms(msg, recipient):
    t = Thread(target=async_send_sms, args=[msg, recipient])
    t.start()