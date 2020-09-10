import os
import time
from app import db, app, mail
from models import User, RalliesAndConventions, Baptism, Death, Promotion, Transfer
from flask import request, render_template
from werkzeug.utils import secure_filename
from flask_mail import Message
from threading import Thread
import urllib
import re
import json
import binascii
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
from file_encrypter import FileEncrypter


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_FILE_EXT = '.jpg'
PROFILE_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "profile_photos")
BAPTISM_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "baptism_photos")
PSEUDO_PROFILE_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "incomplete_reg_acc", "profile_photos")
PSEUDO_DATA_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "incomplete_reg_acc", "data")
PUSH_NOTIF_BASE_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'push_notifications')

def remove_contact_symbols(contact):
    return re.sub(r"\D+", "", contact)

def remove_name_symbols(name):
    return re.sub(r"\W+", "", name)

def pil_image_to_base64(pil_image):
    """
    Convert a pillow image to a base64 image
    """
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue())

def gen_pseudo_id(first_name, last_name, contact_phone_1):
    first_name = remove_name_symbols(first_name)
    last_name = remove_name_symbols(last_name)
    contact_phone_1 = remove_contact_symbols(contact_phone_1)
    return f'{first_name}_{last_name}_{contact_phone_1[-9:]}'

def save_incomplete_reg(data_dict):
    # get the member id
    member_pseudo_id = data_dict["member_id"]
    # get the save the json data
    json_data = json.dumps(data_dict)
    encrypted_json_data = encrypt_json_data(json_data)
    json_filename = f'{member_pseudo_id}.json'
    json_file = open(os.path.join(PSEUDO_DATA_DIR, json_filename), 'wb')
    json_file.write(encrypted_json_data)
    json_file.close()
    # check if the post request has the file part
    img_file = request.files.get("kt_apps_contacts_add_avatar")
    if not img_file:
        return
    # if user does not select file, browser also
    # submit an empty part without filename
    if img_file.filename == '':
        return
    if img_file and allowed_file(img_file.filename):
        # remove existing src and result images
        remove_existing_img(member_pseudo_id, type="incomplete")
        # create unique src image name
        img_name = member_pseudo_id + "_" + get_timestamp() + IMG_FILE_EXT
        # save the source image
        img_file.save(os.path.join(PSEUDO_PROFILE_PHOTOS_DIR, img_name))

def read_incomplete_reg(member_pseudo_id):
    # load the data
    json_filename = f'{member_pseudo_id}.json'
    json_file = open(os.path.join(PSEUDO_DATA_DIR, json_filename), 'rb')
    encrypted_json_data = json_file.read()
    decrypted_json_data = decrypt_json_data(encrypted_json_data)
    json_file.close()
    return json.loads(decrypted_json_data)

def load_img_for_web(first_name, last_name, contact_phone_1):
    # load image
    pseudo_member_id = gen_pseudo_id(first_name, last_name, contact_phone_1)
    img_name = None
    imgs = os.listdir(PSEUDO_PROFILE_PHOTOS_DIR)
    for name in imgs:
        if name.startswith(pseudo_member_id):
            img_name = name
            break
    img = Image.open(os.path.join(PSEUDO_PROFILE_PHOTOS_DIR, img_name))
    # output_str is a base64 string in ascii
    output_str = pil_image_to_base64(img)
    # convert a base64 string in ascii to base64 string in _bytes_
    return binascii.a2b_base64(output_str)

def encrypt_json_data(json_data):
    f = FileEncrypter()
    return f.encrypt(bytes(json_data, encoding='utf-8'))

def decrypt_json_data(encrypted_data):
    f = FileEncrypter()
    return f.decrypt(encrypted_data)
    

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


def upload_profile_photo(member_id):
    """
    Uploads an image file to profile_photos folder
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


def upload_baptism_photo(member_id):
    """
    Uploads an image file to baptism_photos folder
    """
    # check if the post request has the file part
    img_file = request.files.get("certImagInput")
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
        img_file.save(os.path.join(BAPTISM_PHOTOS_DIR, img_name))
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


def remove_existing_img(member_id, type='complete'):
    """
    Removes an already existing image
    """
    dest_dir = PSEUDO_PROFILE_PHOTOS_DIR if type=='incomplete' else PROFILE_PHOTOS_DIR
    imgs = os.listdir(dest_dir)
    for name in imgs:
        if name.startswith(member_id):
            os.remove(os.path.join(dest_dir, name))
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

def read_user_by_member_id(id):
    user = User.query.filter_by(member_id=id).first()
    data = dict()
    if (user):
        data = {'first_name': user.first_name, 'last_name':user.last_name, 'other_names':user.other_names,
        'gender':user.gender, 'occupation':user.occupation, 'assembly':user.assembly, 'contact_1':user.contact_phone_1, 
        'contact_2':user.contact_phone_2, 'dob':'{}-{}-{}'.format(user.dob.year, user.dob.month, user.dob.day), 
        'email':user.email, 'marital_status':user.marital_status, 'ministry':user.ministry, 'group':user.group, 
        'comm_email':user.comm_email,'comm_sms':user.comm_sms, 'comm_phone':user.comm_phone, 
        'address_line_1':user.address_line_1,'address_line_2':user.address_line_2, 'digital_address_code':user.digital_address_code, 
        'region':user.region, 'district':user.district, 'country':user.country, 'img': get_img_path(id)}
    return data

def read_baptism_by_member_id(id):
    baptism = Baptism.query.filter_by(member_id=id).first()
    data = dict()
    if (baptism):
        date_of_baptism = baptism.date_of_baptism
        date_of_baptism = '{}-{}-{}'.format(date_of_baptism.year, date_of_baptism.month, date_of_baptism.day)
        data = {'date_of_baptism': date_of_baptism, 'place_of_baptism': baptism.place_of_baptism, 
        'officiating_minister': baptism.officiating_minister, 'district': baptism.district, 'area': baptism.area, 
        'country': baptism.country, 'img': get_img_path(id, model='baptism')}
    return data

def get_img_path(member_id, type='complete', model="user"):
    """
    Removes an already existing image
    """
    dest_dir = PSEUDO_PROFILE_PHOTOS_DIR if type=='incomplete' else PROFILE_PHOTOS_DIR
    if model == "baptism":
        dest_dir = BAPTISM_PHOTOS_DIR
    imgs = os.listdir(dest_dir)
    for name in imgs:
        if name.startswith(member_id):
            return os.path.join(dest_dir, name)
    return ""


def get_rc_id():
    """
    Get the rallies and conventions id for the most recently submitted data
    """
    return db.session.query(db.func.max(RalliesAndConventions.cr_id)).scalar()

def get_death_id():
    """
    Get the death id for the most recently submitted data
    """
    return db.session.query(db.func.max(Death.id)).scalar()

def get_promotion_id():
    """
    Get the promotion id for the most recently submitted data
    """
    return db.session.query(db.func.max(Promotion.id)).scalar()

def get_transfer_id():
    """
    Get the Transfer id for the most recently submitted data
    """
    return db.session.query(db.func.max(Transfer.id)).scalar()

def set_date_time(start_date_time):
    _date, _time = start_date_time.split()
    _date = _date.split('-')
    _time = _time.split(':')
    return datetime(int(_date[0]), int(_date[1]), int(_date[2]), int(_time[0]), int(_time[1]))


def get_notif_msg_id(dir_name):
    """
    Gets the next push notification message id
    """
    return len(os.listdir(os.path.join(PUSH_NOTIF_BASE_DIR, dir_name))) + 1


def save_notif_msg(msg_data, dir_name):
    # double check message id
    msg_data["message_id"] = get_notif_msg_id(dir_name)
    # get the save the json data
    json_data = json.dumps(msg_data)
    encrypted_json_data = encrypt_json_data(json_data)
    json_filename = f'{msg_data["message_id"]}.json'
    json_file = open(os.path.join(PUSH_NOTIF_BASE_DIR, dir_name, json_filename), 'wb')
    json_file.write(encrypted_json_data)
    json_file.close()


def read_notif_msg(message_id, dir_name):
    # load the data
    json_filename = f'{message_id}.json'
    json_file = open(os.path.join(PUSH_NOTIF_BASE_DIR, dir_name, json_filename), 'rb')
    encrypted_json_data = json_file.read()
    decrypted_json_data = decrypt_json_data(encrypted_json_data)
    json_file.close()
    return json.loads(decrypted_json_data)

def member_id_exists(member_id, table="user"):
    #Tables involved: death, baptism
    if table == 'death' and Death.query.filter_by(member_id=member_id).first():
        return True
    if table == 'baptism' and Baptism.query.filter_by(member_id=member_id).first():
        return True
    return False