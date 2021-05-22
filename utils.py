import os
import time
import shutil
import random
import string

#from sqlalchemy.util.langhelpers import group_expirable_memoized_property
from sqlalchemy import func
from app import db, app, mail
from models import Accessibility, User, Baptism, RalliesAndConventions, Dedication, Death, Promotion, Transfer, Birth, Attendance
from flask import request, render_template
from werkzeug.utils import secure_filename
from flask_mail import Message
from threading import Thread
import urllib
import re
import json
from urllib.parse import urlparse
import binascii
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
import urllib
from file_encrypter import FileEncrypter
from constants import *


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_FILE_EXT = '.jpg'
PROFILE_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "profile_photos")
BAPTISM_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "baptism_photos")
PSEUDO_PROFILE_PHOTOS_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "incomplete_reg_acc", "profile_photos")
PSEUDO_DATA_DIR = os.path.join(app.config['UPLOAD_FOLDER'], "incomplete_reg_acc", "data")
PUSH_NOTIF_BASE_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'push_notifications')
ASSEMBLY_CONFIG_BASE_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'assembly_config')
ASSEMBLY_DEACTIVATED_BASE_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'deactivated_assembly')
ATTENDANCE_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'attendance')
PERMISSION_MAP = dict(chief='Chief Finance', super='Super Admin', admin=f'Sub Admin', finance=f'Finance Officer')

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

def generate_password(length=8):
    chars = string.ascii_letters + string.punctuation + string.digits
    return ''.join(random.choice(chars) for i in range(length))

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
    decrypted_json_data = json.loads(decrypted_json_data)
    decrypted_json_data['img'] = get_img_path(member_pseudo_id, type='incomplete')
    return decrypted_json_data

def load_all_incomplete_reg():
    """
    Returns all the incomplete registration account filenames (pseudo ids)
    """
    filenames = os.listdir(PSEUDO_DATA_DIR)
    try:
        filenames.remove("constant_empty_json_file.json")
    except:
        pass
    incomplete_reg_data = []
    for name in filenames:
        pseudo_id = name.replace(".json", "")
        data = read_incomplete_reg(pseudo_id)
        incomplete_reg_data.append(data)
    return incomplete_reg_data

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


def gen_id(first_name, other_names, last_name):
    """
    This generates the ID for a user
    """
    first_name = first_name[0]
    other_names = (other_names[0] if other_names else "")
    last_name = re.sub(r"[^\w]", "", last_name)
    member_id = first_name + other_names + last_name
    existing_id_count = db.session.query(User).filter(User.member_id.ilike(f'{member_id}%')).count()
    member_id = (member_id if existing_id_count == 0 else f'{member_id}{to_given_length(existing_id_count, 3)}')
    return member_id.lower()


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


def upload_attendance(assembly_name):
    """
    Uploads attendance
    """
    # check if the post request has the file part
    attendance_file = request.files.get("attendance_file")
    if not attendance_file:
        return NO_FILE_ERROR
    # if user does not select file, browser also
    # submit an empty part without filename
    if attendance_file.filename == '':
        return NO_FILE_ERROR
    # get file extension
    ext = attendance_file.filename.lower().split('.')[-1]
    if attendance_file and ext == 'csv':
        # create unique file name
        filename = get_attendance_filename(assembly_name) + '.csv'
        # save
        attendance_file.save(os.path.join(ATTENDANCE_DIR, filename))
        # add attendance to database 
        return add_attendance_to_db(filename)
    # return the index page if the form is not submitted rightly
    return INVALID_FORMAT_ERROR


def add_attendance_to_db(filename):
    """
    Adds an attendance data to the database
    """
    try:
        attendance_file = open(os.path.join(ATTENDANCE_DIR, filename), 'r')
        attendance_data = attendance_file.readlines()
        attendance_file.close()
        for i, row in enumerate(attendance_data):
            name, member_id, event, date, status, time_in, time_out = row.split(",")
            date = date.split('-')[0].strip()
            date = date.replace('/', '-')
            #Skip the head of the csv file
            if i > 0:
                #compare the first lines of last file and new file to be submitted 
                date_for_comp = date.split('-')
                date_for_comp = datetime(int(date_for_comp[2]), int(date_for_comp[1]), int(date_for_comp[0]))
                record_exists = Attendance.query.filter_by(member_id=member_id, event=event,date=date_for_comp, status=status, time_in=time_in, time_out=time_out).first()
                if record_exists:
                    row_dict = {
                        "member_id": member_id,
                        "event": event,
                        "date": date_for_comp,
                        "status": status,
                        "time_in": time_in,
                        "time_out": time_out,
                    }
                    Attendance.query.filter_by(member_id=member_id, event=event,date=date_for_comp, status=status, time_in=time_in, time_out=time_out).update(row_dict)
                    db.session.commit()
                else:
                    attendance = Attendance(member_id=member_id, event=event, status=status, time_in=time_in, time_out=time_out)
                    attendance.set_date(date)
                    db.session.add(attendance)
        db.session.commit()
        return SUCCESS
    except Exception as e:
        print(e)
        return FATAL_ERROR


def get_attendance_filename(assembly_name):
    """
    Returns the filename of the attendance file
    """
    assembly_name = assembly_name.lower().replace(' ', '_')
    count = str(len(os.listdir(ATTENDANCE_DIR)) + 1)
    timestamp = get_timestamp()
    return "_".join([count, timestamp]) + '_' + assembly_name


def remove_existing_attendance(filename):
    """
    Removes an already existing attendance
    """
    files = os.listdir(ATTENDANCE_DIR)
    for name in files:
        if name.startswith(filename):
            os.remove(os.path.join(ATTENDANCE_DIR, name))
            break
    

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

def send_email(recipient, msg_content):
    subject = app.config['MAIL_SENDER_NAME']
    msg = Message(subject, recipients=[recipient])
    msg.html = msg_content
    t = Thread(target=async_send_mail, args=[msg])
    t.start()
    return t

def read_user_by_member_id(id):
    user = User.query.filter_by(member_id=id).first()
    data = dict()
    if (user):
        data = {'member_id': id, 'first_name': user.first_name, 'last_name':user.last_name, 'other_names':user.other_names,
        'gender':user.gender, 'occupation':user.occupation, 'assembly':user.assembly, 'contact_1':user.contact_phone_1, 
        'contact_2':user.contact_phone_2, 'dob':'{}-{}-{}'.format(user.dob.year, to_given_length(user.dob.month, 2), to_given_length(user.dob.day, 2)), 
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
    return "/static/assets/media/users/thecopkadna-users.png"


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


def save_assembly_config(config_dict):
    # get the save the json data
    json_data = json.dumps(config_dict)
    encrypted_json_data = encrypt_json_data(json_data)
    json_filename = 'config.json'
    dir_name = re.sub(r"[\+\-\s]+", "_", config_dict["assembly_name"].lower())
    dir_path = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    json_file = open(os.path.join(dir_path, json_filename), 'wb')
    json_file.write(encrypted_json_data)
    json_file.close()


def read_assembly_config(assembly_name, active=True):
    # load the data
    json_filename = 'config.json'
    dir_name = re.sub(r"[\+\-\s]+", "_", assembly_name.lower())
    if active:
        json_file = open(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, json_filename), 'rb')
    else:
        json_file = open(os.path.join(ASSEMBLY_DEACTIVATED_BASE_DIR, dir_name, json_filename), 'rb')
    encrypted_json_data = json_file.read()
    decrypted_json_data = decrypt_json_data(encrypted_json_data)
    json_file.close()
    decrypted_json_data = json.loads(decrypted_json_data)
    # load the document and file paths
    decrypted_json_data['logo'] = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'logo.jpg') if os.path.exists(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'logo.jpg')) else ''
    decrypted_json_data['letter_head'] = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'letter_head.jpg') if os.path.exists(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'letter_head.jpg')) else ''
    decrypted_json_data['dedication_cert_template'] = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'dedication_cert_template.pdf') if os.path.exists(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'dedication_cert_template.pdf')) else ''
    decrypted_json_data['baptism_cert_template'] = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'baptism_cert_template.pdf') if os.path.exists(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'baptism_cert_template.pdf')) else ''
    return decrypted_json_data


def upload_assembly_config_files(assembly_name):
    """
    Uploads the letter head, baptism and dedication certificates templates to the assembly config folder
    """
    # get the assembly folder name
    dir_name = re.sub(r"[\s]+", "_", assembly_name.lower())
    dir_path = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    # check if the post request has the file part
    logo_img = request.files.get("logo_upload")
    letter_head_img = request.files.get("letter_head")
    baptism_cert_template = request.files.get("baptism_cert_template")
    dedication_cert_template = request.files.get("dedication_cert_template")
    # if all the files are not provided, return
    if not logo_img and not letter_head_img and not baptism_cert_template and not dedication_cert_template:
        return False
    # if user does not select file, browser also
    # submit an empty part without filename
    missing_files = []
    if logo_img:
        if logo_img.filename == '':
            missing_files.append('logo_img')
    else:
        missing_files.append('logo_img')
    if letter_head_img:
        if letter_head_img.filename == '':
            missing_files.append('letter_head_img')
    else:
        missing_files.append('letter_head_img')
    if baptism_cert_template:
        if baptism_cert_template.filename == '':
            missing_files.append('baptism_cert_template')
    else:
        missing_files.append('baptism_cert_template')
    if dedication_cert_template:
        if dedication_cert_template.filename == '':
            missing_files.append('dedication_cert_template')
    else:
        missing_files.append('dedication_cert_template')
    # save the files
    if (logo_img and allowed_file(logo_img.filename)):
        logo_img.save(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'logo' + IMG_FILE_EXT))
    if (letter_head_img and allowed_file(letter_head_img.filename)) and not missing_files.__contains__('letter_head_img'):
        letter_head_img.save(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'letter_head' + IMG_FILE_EXT))
    if (baptism_cert_template and '.' in baptism_cert_template.filename and baptism_cert_template.filename.rsplit('.', 1)[1].lower() == "pdf") and not missing_files.__contains__('baptism_cert_template'):
        baptism_cert_template.save(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'baptism_cert_template.pdf'))
    if (dedication_cert_template and '.' in dedication_cert_template.filename and baptism_cert_template.filename.rsplit('.', 1)[1].lower() == "pdf") and not missing_files.__contains__('dedication_cert_template'):
        dedication_cert_template.save(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name, 'dedication_cert_template.pdf'))

    # return the index page if the form is not submitted rightly
    return False


def load_assembly_data():
    assembly_names = []
    ministry_names = []
    group_names = {}
    for dir_name in os.listdir(ASSEMBLY_CONFIG_BASE_DIR):
        assembly_name = read_assembly_config(dir_name)['assembly_name']
        assembly_names.append(assembly_name)
        ministry_names.extend(read_assembly_config(dir_name)['ministry'])
        group_names[assembly_name] = read_assembly_config(dir_name)['group']
    ministry_names = list(set(ministry_names))
    return assembly_names, ministry_names, group_names


def get_latest_updates(assembly_name):
    assembly_group_data = read_assembly_config(assembly_name)['group']
    assembly_name = ' '.join([p.capitalize().strip() for p in assembly_name.split('_')])
    bible_studies_groups = len(assembly_group_data)
    water_baptism_count = db.session.query(Baptism, User).join(User).filter_by(assembly=assembly_name).count()
    birth_count = Birth.query.filter_by(assembly=assembly_name).count()
    death_count = db.session.query(Death, User).join(User).filter_by(assembly=assembly_name).count()
    rallies_and_conventions_count = RalliesAndConventions.query.filter(RalliesAndConventions.assembly.ilike(f'%{assembly_name}%')).count()
    transfer_count = db.session.query(Transfer, User).join(User).filter_by(assembly=assembly_name).count()
    promotion_count = db.session.query(Promotion, User).join(User).filter_by(assembly=assembly_name).count()
    transfer_and_promotion_count = transfer_count + promotion_count
    dedication_count = Dedication.query.filter_by(assembly=assembly_name).count()
    member_count = User.query.filter_by(assembly=assembly_name).count()
    latest_updates = {
        "water_baptism":water_baptism_count,
        "births":birth_count,
        "deaths":death_count,
        "rallies_and_conventions":rallies_and_conventions_count,
        "transfers_and_promotions":transfer_and_promotion_count,
        "dedications":dedication_count,
        "bible_studies_groups": bible_studies_groups,
        "member_count": member_count,
    }
    return latest_updates


def get_attendance_notifs(assembly):
    assembly_dir_name = assembly.lower().replace(' ', '_')
    filenames_original = os.listdir(ATTENDANCE_DIR)
    if not assembly.strip() == '%':
        filenames_original = [name for name in filenames_original if name.__contains__(assembly_dir_name)]
    filenames_original = sorted(filenames_original, key=lambda x: int(x.split('_')[0]), reverse=True)[:10]
    filenames = sorted(filenames_original, key=lambda x: int(x.split('_')[0]), reverse=True)
    filenames = [name.split('.')[0] for name in filenames]
    dates_assembly_names_list = [name.split('_')[1:] for name in filenames]
    msgs = []
    for i in range(len(filenames)):
        msg_data = dict()
        # compose the message
        dt = datetime(int(dates_assembly_names_list[i][0]), int(dates_assembly_names_list[i][1]), int(dates_assembly_names_list[i][2]), int(dates_assembly_names_list[i][3]), int(dates_assembly_names_list[i][4]), int(dates_assembly_names_list[i][5]))
        assembly_name = ' '.join([p.capitalize() for p in dates_assembly_names_list[i][6:]])
        msg_data['bva_data'] = f'/static/storage/attendance/{filenames_original[i]}'
        msg_data['msg'] = f"BVA for {assembly_name} submitted successfully on {dt.strftime('%A, %B %d, %Y')}"
        # get the event
        attendance_file = open(os.path.join(ATTENDANCE_DIR, filenames_original[i]), 'r')
        attendance_data = attendance_file.readlines()
        for i, line in enumerate(attendance_data):
            if i > 0:
                msg_data['event_date'] = line.split(',')[3].split('-')[0].strip()
                break
        attendance_file.close()
        msgs.append(msg_data)
    return msgs


def get_statistical_updates(assembly_name):
    stats_data_dict = dict()
    # get dates
    date_now = datetime.now()
    date_13_years_ago = datetime(date_now.year - 13, date_now.month, date_now.day)
    date_20_years_ago = datetime(date_now.year - 20, date_now.month, date_now.day)
    date_36_years_ago = datetime(date_now.year - 36, date_now.month, date_now.day)
    
    # get dedicated children membership
    ded_child_below_13_yrs_dict = dict()
    ded_child_below_13_yrs_dict['male'] = 'N/A'
    ded_child_below_13_yrs_dict['female'] = 'N/A'
    if assembly_name == '%':
        ded_child_below_13_yrs_dict['total'] = str(Dedication.query.filter(Dedication.child_dob > date_13_years_ago).count())
    else:
        ded_child_below_13_yrs_dict['total'] = str(Dedication.query.filter(Dedication.child_dob > date_13_years_ago, Dedication.assembly==assembly_name).count())
    stats_data_dict['1'] = ded_child_below_13_yrs_dict

    # get teenagers 13 to 19 years
    teens_13_to_19_yrs_dict = dict()
    if assembly_name == '%':
        teens_13_to_19_yrs_dict['male'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_20_years_ago, User.gender=='Male').count())
        teens_13_to_19_yrs_dict['female'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_20_years_ago, User.gender=='Female').count())
    else:
        teens_13_to_19_yrs_dict['male'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_20_years_ago, User.gender=='Male', User.assembly==assembly_name).count())
        teens_13_to_19_yrs_dict['female'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_20_years_ago, User.gender=='Female', User.assembly==assembly_name).count())
    teens_13_to_19_yrs_dict['total'] = str(int(teens_13_to_19_yrs_dict['male']) + int(teens_13_to_19_yrs_dict['female']))
    stats_data_dict['2'] = teens_13_to_19_yrs_dict

    # young adults 20 to 35 years
    adults_20_to_35_yrs_dict = dict()
    if assembly_name == '%':
        adults_20_to_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_20_years_ago, User.dob > date_36_years_ago, User.gender=='Male').count())
        adults_20_to_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_20_years_ago, User.dob > date_36_years_ago, User.gender=='Female').count())
    else:
        adults_20_to_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_20_years_ago, User.dob > date_36_years_ago, User.gender=='Male', User.assembly==assembly_name).count())
        adults_20_to_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_20_years_ago, User.dob > date_36_years_ago, User.gender=='Female', User.assembly==assembly_name).count())
    adults_20_to_35_yrs_dict['total'] = str(int(adults_20_to_35_yrs_dict['male']) + int(adults_20_to_35_yrs_dict['female']))
    stats_data_dict['3'] = adults_20_to_35_yrs_dict

    # youth from 13 to 35 years
    adults_20_to_35_yrs_dict = dict()
    if assembly_name == '%':
        adults_20_to_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_36_years_ago, User.gender=='Male', ).count())
        adults_20_to_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_36_years_ago, User.gender=='Female', ).count())
    else:
        adults_20_to_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_36_years_ago, User.gender=='Male', User.assembly==assembly_name).count())
        adults_20_to_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_13_years_ago, User.dob > date_36_years_ago, User.gender=='Female', User.assembly==assembly_name).count())
    adults_20_to_35_yrs_dict['total'] = str(int(adults_20_to_35_yrs_dict['male']) + int(adults_20_to_35_yrs_dict['female']))
    stats_data_dict['4'] = adults_20_to_35_yrs_dict

    # adults above 35
    adults_above_35_yrs_dict = dict()
    if assembly_name == '%':
        adults_above_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_36_years_ago, User.gender=='Male').count())
        adults_above_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_36_years_ago, User.gender=='Female').count())
    else:
        adults_above_35_yrs_dict['male'] = str(User.query.filter(User.dob <= date_36_years_ago, User.gender=='Male', User.assembly==assembly_name).count())
        adults_above_35_yrs_dict['female'] = str(User.query.filter(User.dob <= date_36_years_ago, User.gender=='Female', User.assembly==assembly_name).count())
    adults_above_35_yrs_dict['total'] = str(int(adults_above_35_yrs_dict['male']) + int(adults_above_35_yrs_dict['female']))
    stats_data_dict['5'] = adults_above_35_yrs_dict

    # total adults 13 and above
    total_adults_13_and_above = str(User.query.filter(User.dob <= date_13_years_ago, User.assembly==assembly_name).count())
    stats_data_dict['6'] = total_adults_13_and_above

    # overall membership
    overall_membership = str(int(ded_child_below_13_yrs_dict['total']) + int(total_adults_13_and_above))
    stats_data_dict['7'] = overall_membership

    # officers
    officers_dict = dict()
    officers_dict['ministers'] = 'N/A'
    officers_dict['ministers_wives'] = 'N/A'
    officers_dict['retired_ministers'] = 'N/A'
    officers_dict['rtd_ministers_wives'] = 'N/A'
    officers_dict['elders'] = 'N/A'
    officers_dict['deacons'] = 'N/A'
    officers_dict['deaconesses'] = 'N/A'
    officers_dict['leaders'] = 'N/A'
    stats_data_dict['8'] = officers_dict

    # rallies and conventions count
    outreach_programmes = str(RalliesAndConventions.query.filter(RalliesAndConventions.assembly.ilike(f'%{assembly_name}%')).count())
    stats_data_dict['9'] = outreach_programmes

    # adult souls won
    adult_souls_won = 'N/A'
    stats_data_dict['10'] = adult_souls_won

    # number of souls won through gospel sunday morning
    souls_won_on_gospel_sunday_morning = 'N/A'
    stats_data_dict['11'] = souls_won_on_gospel_sunday_morning

    # new converts baptized in water
    new_converts_baptized_in_water = str(db.session.query(Baptism, User).join(User).filter(User.assembly==assembly_name).count())
    stats_data_dict['12'] = new_converts_baptized_in_water

    # new converts baptized in water
    new_converts_baptized_in_holy_spirit = 'N/A'
    stats_data_dict['13'] = new_converts_baptized_in_holy_spirit

    # new converts baptized in water
    old_adults_baptized_in_holy_spirit = 'N/A'
    stats_data_dict['14'] = old_adults_baptized_in_holy_spirit

    # transfers in 
    transfers_in_dict = dict()
    if assembly_name == '%':
        transfers_in_dict['teens_13_19'] = str(Transfer.query.filter(Transfer.transfered_to==assembly_name, Transfer.age >= 13, Transfer.age < 20).count())
        transfers_in_dict['young_adults_20_35'] = str(Transfer.query.filter(Transfer.transfered_to==assembly_name, Transfer.age >= 20, Transfer.age < 36).count())
        transfers_in_dict['adults_36'] = str(Transfer.query.filter(Transfer.transfered_to==assembly_name, Transfer.age >= 36).count())
    else:
        transfers_in_dict['teens_13_19'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_to==assembly_name, Transfer.age >= 13, Transfer.age < 20, User.assembly==assembly_name).count())
        transfers_in_dict['young_adults_20_35'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_to==assembly_name, Transfer.age >= 20, Transfer.age < 36, User.assembly==assembly_name).count())
        transfers_in_dict['adults_36'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_to==assembly_name, Transfer.age >= 36, User.assembly==assembly_name).count())
    transfers_in_dict['total'] = str(int(transfers_in_dict['teens_13_19'])+int(transfers_in_dict['young_adults_20_35'])+int(transfers_in_dict['adults_36']))
    stats_data_dict['15'] = transfers_in_dict

    #transfers out
    transfers_out_dict = dict()
    if assembly_name == '%':
        transfers_out_dict['teens_13_19'] = str(Transfer.query.filter(Transfer.transfered_from==assembly_name, Transfer.age >= 13, Transfer.age < 20).count())
        transfers_out_dict['young_adults_20_35'] = str(Transfer.query.filter(Transfer.transfered_from==assembly_name, Transfer.age >= 20, Transfer.age < 36).count())
        transfers_out_dict['adults_36'] = str(Transfer.query.filter(Transfer.transfered_from==assembly_name, Transfer.age >= 36).count())
    else:
        transfers_out_dict['teens_13_19'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_from==assembly_name, Transfer.age >= 13, Transfer.age < 20, User.assembly==assembly_name).count())
        transfers_out_dict['young_adults_20_35'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_from==assembly_name, Transfer.age >= 20, Transfer.age < 36, User.assembly==assembly_name).count())
        transfers_out_dict['adults_36'] = str(db.session.query(Transfer, User).join(User).filter(Transfer.transfered_from==assembly_name, Transfer.age >= 36, User.assembly==assembly_name).count())
    transfers_out_dict['total'] = str(int(transfers_out_dict['teens_13_19'])+int(transfers_out_dict['young_adults_20_35'])+int(transfers_out_dict['adults_36']))
    stats_data_dict['16'] = transfers_in_dict

    # back sliders 
    backsliders_dict = dict()
    backsliders_dict['won_back'] = 'N/A'
    backsliders_dict['being_followed'] = 'N/A'
    stats_data_dict['17'] = backsliders_dict

    # deaths
    user_death_data = None
    if assembly_name == '%':
        user_death_data = db.session.query(Death, User).join(User).all()
    else:
        user_death_data = db.session.query(Death, User).join(User).filter(User.assembly==assembly_name).all()
    adult_deaths = 0
    for death, user in user_death_data:
        aged = (death.death_date - user.dob).days / 365
        if aged >= 20:
            adult_deaths += 1
    stats_data_dict['18'] = adult_deaths

    # number of home cells
    number_of_home_cells = 'N/A'
    stats_data_dict['19'] = number_of_home_cells

    # number of members in home cells
    number_of_members_in_home_cells_dict = dict()
    number_of_members_in_home_cells_dict['male'] = 'N/A'
    number_of_members_in_home_cells_dict['female'] = 'N/A'
    number_of_members_in_home_cells_dict['total'] = 'N/A' # number_of_members_in_home_cells_dict['male'] + number_of_members_in_home_cells_dict['female'] = 'N/A'
    stats_data_dict['20'] = number_of_members_in_home_cells_dict

    # number of home cells held
    number_of_home_cells_held = 'N/A'
    stats_data_dict['21'] = number_of_home_cells_held

    # number of bible study groups
    number_of_bible_study_groups = 0
    if assembly_name == '%':
        _, _, groups_dict = load_assembly_data()
        all_groups = []
        for g in groups_dict.values():
            all_groups.extend(g)
        number_of_bible_study_groups = len(all_groups)
    else:
        latest_updates = get_latest_updates('Emmanuel English Assembly')
        number_of_bible_study_groups = latest_updates['bible_studies_groups']
    stats_data_dict['22'] = number_of_bible_study_groups

    # number of trained bible study group teachers/leaders
    number_of_bible_study_teachers = 'N/A'
    stats_data_dict['23'] = number_of_bible_study_teachers

    # number of active members in bible studies
    number_of_active_members_bible_studies = 'N/A'
    stats_data_dict['24'] = number_of_active_members_bible_studies

    # number of sunday morning bible studies held
    number_of_sunday_morning_bible_studies_held = 'N/A'
    stats_data_dict['25'] = number_of_sunday_morning_bible_studies_held

    # number of public reading sessions held
    number_of_public_reading_sessions_held = 'N/A'
    stats_data_dict['26'] = number_of_public_reading_sessions_held

    # Adult church attendance 31 Dec.
    church_attendance_31_dec = 'N/A'
    stats_data_dict['27'] = church_attendance_31_dec

    # avg sunday morning church attendance
    avg_sunday_morning_church_attendance = 'N/A'
    stats_data_dict['28'] = avg_sunday_morning_church_attendance

    # avg attendance in communion sundays
    avg_attendance_communion_sundays = 'N/A'
    stats_data_dict['29'] = avg_attendance_communion_sundays

    # avg lord's supper participants
    avg_lords_supper_participants = 'N/A'
    stats_data_dict['30'] = avg_lords_supper_participants

    # num attending new converts class
    num_attending_new_converts_class = 'N/A'
    stats_data_dict['31'] = num_attending_new_converts_class

    # new converts retained in church
    new_converts_retained = 'N/A'
    stats_data_dict['32'] = new_converts_retained

    # num of times p/elder visited new converts
    num_of_times_p_elder_visited_new_converts = 'N/A'
    stats_data_dict['33'] = num_of_times_p_elder_visited_new_converts

    #num of times new convert class held
    num_of_times_new_converts_class_held = 'N/A'
    stats_data_dict['34'] = num_of_times_new_converts_class_held

    # num of mid-week church study
    num_of_mid_week_church_study = 'N/A'
    stats_data_dict['35'] = num_of_mid_week_church_study

    # avg attendance on friday prayer meeting
    avg_attendance_on_friday_prayer_meetings = 'N/A'
    stats_data_dict['36'] = avg_attendance_on_friday_prayer_meetings

    # num of holy ghost prayer sessions held
    num_of_holy_ghost_prayer_sess_held = 'N/A'
    stats_data_dict['37'] = num_of_holy_ghost_prayer_sess_held

    # num of times family/marriage life teachings held
    num_of_times_teachings_on_family_and_marriage_held = 'N/A'
    stats_data_dict['38'] = num_of_times_teachings_on_family_and_marriage_held

    # num of marriages blessed 
    num_of_marriages_blessed = 'N/A'
    stats_data_dict['39'] = num_of_marriages_blessed

    # num of adult and children service held
    num_of_adult_and_children_service_held = 'N/A'
    stats_data_dict['40'] = num_of_adult_and_children_service_held

    # num of children dedicated
    num_of_children_dedicated = 0
    if assembly_name == '%':
        num_of_children_dedicated = str(Dedication.query.count())
    else:
        num_of_children_dedicated = str(Dedication.query.filter(Dedication.assembly==assembly_name).count())
    num_of_children_dedicated = str(Dedication.query.count())
    stats_data_dict['41'] = num_of_children_dedicated

    # children won for christ and retained
    children_won_and_retained = 'N/A'
    stats_data_dict['42'] = children_won_and_retained

    # children baptized with the holy spirit
    children_baptized_with_the_holy_spirit = 'N/A'
    stats_data_dict['43'] = children_baptized_with_the_holy_spirit

    # children baptized with water
    children_baptized_in_water = 'N/A'
    stats_data_dict['44'] = children_baptized_in_water

    # num of children ministry teachers
    num_of_children_ministry_teachers = 'N/A'
    stats_data_dict['45'] = num_of_children_ministry_teachers

    # num of children attending children ministry but not dedicated
    non_dedicated_children_in_CM = 'N/A'
    stats_data_dict['46'] = non_dedicated_children_in_CM

    # children transfered in
    children_transfered_in = 'N/A'
    stats_data_dict['47'] = children_transfered_in

    # children transfered out
    children_transfered_out = 'N/A'
    stats_data_dict['48'] = children_transfered_out

    # births
    num_births = 0
    if assembly_name == '%':
        num_births = str(Birth.query.count())
    else:
        num_births = str(Birth.query.filter(Birth.assembly == assembly_name).count())
    stats_data_dict['49'] = num_births

    # deaths
    num_deaths = 0
    if assembly_name == '%':
        num_deaths = str(Death.query.count())
    else:
        num_deaths = str(db.session.query(Death, User).join(User).filter(User.assembly == assembly_name).count())
    stats_data_dict['50'] = num_deaths

    # number of classes held
    num_of_classes_held_dict = dict()
    num_of_classes_held_dict['women'] = 'N/A'
    num_of_classes_held_dict['men'] = 'N/A'
    num_of_classes_held_dict['youth'] = 'N/A'
    num_of_classes_held_dict['evangelism'] = 'N/A'
    num_of_classes_held_dict['children'] = 'N/A'
    stats_data_dict['51'] = num_of_classes_held_dict

    # number of active members in classes, ministries
    num_of_active_members_classes_ministries_dict = dict()
    num_of_active_members_classes_ministries_dict['women'] = 'N/A'
    num_of_active_members_classes_ministries_dict['men'] = 'N/A'
    num_of_active_members_classes_ministries_dict['youth'] = 'N/A'
    num_of_active_members_classes_ministries_dict['evangelism'] = 'N/A'
    num_of_active_members_classes_ministries_dict['children'] = 'N/A'
    stats_data_dict['52'] = num_of_active_members_classes_ministries_dict

    # number of visits by ministers
    num_of_visits_by_ministers_dict = dict()
    num_of_visits_by_ministers_dict['women'] = 'N/A'
    num_of_visits_by_ministers_dict['men'] = 'N/A'
    num_of_visits_by_ministers_dict['youth'] = 'N/A'
    num_of_visits_by_ministers_dict['evangelism'] = 'N/A'
    num_of_visits_by_ministers_dict['children'] = 'N/A'
    stats_data_dict['53'] = num_of_visits_by_ministers_dict

    # return data
    return stats_data_dict


def assemblies_registration_summary():
    """
    Gets summary data for the assemblies
    """
    member_count = db.session.query(User.assembly, func.count(User.assembly)).group_by(User.assembly).all()
    for i, count in enumerate(member_count):
        member_count[i] = (i + 1, count[0], count[1])
    data = {
        "area": "Kwadaso",
        "district": "Kwadaso Agric",
        "member_count": member_count
    }
    return data

def activate_assembly(assembly_name):
    """
    Activates an assembly
    """
    deactivated_assembly_dir = os.path.join(ASSEMBLY_DEACTIVATED_BASE_DIR, assembly_name)
    specific_assembly_dir = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, assembly_name)
    dest = shutil.move(deactivated_assembly_dir, specific_assembly_dir)

    return dest

def deactivate_assembly(assembly_name):
    """
    Deactivates an assembly
    """
    specific_assembly_dir = os.path.join(ASSEMBLY_CONFIG_BASE_DIR, assembly_name)
    destination = os.path.join(ASSEMBLY_DEACTIVATED_BASE_DIR, assembly_name)

    dest = shutil.move(specific_assembly_dir, destination)

    return dest
    
def get_assembly_ui_data():
    """
    Gets data the assembly ui panel
    """
    assembly_ui_data = []
    for dir_name in os.listdir(ASSEMBLY_CONFIG_BASE_DIR):
        if os.path.isdir(os.path.join(ASSEMBLY_CONFIG_BASE_DIR, dir_name)):
            assembly_dict = dict()
            assembly_dict['toggle_activate_btn_label'] = 'Deactivate'
            assembly_dict['assembly_name'] = read_assembly_config(dir_name)['assembly_name']
            assembly_dict['ministries'] = str(len(read_assembly_config(dir_name)['ministry']))
            assembly_dict['groups'] = str(len(read_assembly_config(dir_name)['group']))
            assembly_dict['total_registered'] = str(User.query.filter_by(assembly=assembly_dict['assembly_name']).count())
            assembly_dict['admins'] = '2' #str(Admins.query.filter_by(assembly=assembly_dict['assembly_name']).count())
            assembly_ui_data.append(assembly_dict)
    for dir_name in os.listdir(ASSEMBLY_DEACTIVATED_BASE_DIR):
        if os.path.isdir(os.path.join(ASSEMBLY_DEACTIVATED_BASE_DIR, dir_name)):
            assembly_dict = dict()
            assembly_dict['toggle_activate_btn_label'] = 'Activate'
            assembly_dict['assembly_name'] = read_assembly_config(dir_name, active=False)['assembly_name']
            assembly_dict['ministries'] = str(len(read_assembly_config(dir_name, active=False)['ministry']))
            assembly_dict['groups'] = str(len(read_assembly_config(dir_name, active=False)['group']))
            assembly_dict['total_registered'] = str(User.query.filter_by(assembly=assembly_dict['assembly_name']).count())
            assembly_dict['admins'] = '2' #str(Admins.query.filter_by(assembly=assembly_dict['assembly_name']).count())
            assembly_ui_data.append(assembly_dict)
    return assembly_ui_data

def read_accessibility_by_member_id(id):
    accessibility = Accessibility.query.filter_by(member_id=id).first()
    data = dict()
    if (accessibility):
        permission_map = dict(chief='Chief Finance', super='Super Admin', admin=f'Sub Admin - {accessibility.assembly}', finance=f'Finance Officer - {accessibility.assembly}')
        permission_edited = permission_map[accessibility.permission.split('_')[0]]
        data = {'member_id': id, 'permission': accessibility.permission, 'permission_edited': permission_edited, 'assembly':accessibility.assembly, 'assembly_status':accessibility.assembly_status}
    return data

def remove_access(member_id):
    """
    Delete access privileges given to sub-admins
    """
    #print(member_id)
    #sub_admin = Accessibility.query.get(member_id)
    sub_admin = Accessibility.query.filter_by(member_id=member_id).first()
    #print(sub_admin)
    db.session.delete(sub_admin)
    db.session.commit()
    return sub_admin
 

def get_notif_count():
    """
    Get the total number of notifications
    """
    counter = 0
    for dir_name in os.listdir(PUSH_NOTIF_BASE_DIR):
        counter += len(os.listdir(os.path.join(PUSH_NOTIF_BASE_DIR, dir_name)))
    return counter


def valid_next_param(next_param):
    return (True if urlparse(next_param).netloc.strip() == '' else False)


def check_sms_balance():
    """
    Returns the SMS balance
    """
    try:
        params = {'key': app.config['SMS_API_KEY']}
        params = urllib.parse.urlencode(params)
        url = f'https://apps.mnotify.net/smsapi/balance?{params}'
        balance = urllib.request.urlopen(url).read()
        return balance.decode()
    except Exception as e:
        print(e)


def async_send_sms(recipient_contact, member_id, password):
    """
    Sends SMS to the selected member
    """
    try:
        message = f'Membership Account Details\n\nMEMBER ID: {member_id}\nPASSWORD: {password}'
        params = {'key': app.config['SMS_API_KEY'], 'to': recipient_contact, 'msg': message, 'sender_id': app.config['SMS_SENDER_ID']}
        params = urllib.parse.urlencode(params)
        url = f'https://apps.mnotify.net/smsapi?{params}'
        return_code = urllib.request.urlopen(url).read()
        if int(return_code) == 1000:
            print(f'Message sent successfully to {recipient_contact}')
        else:
            print(f'Message not sent to {recipient_contact}')
    except Exception as e:
        print(e)

def send_sms(recipient_contact, member_id, password):
    """
    Starts the SMS thread
    """
    t = Thread(target=async_send_sms, args=[recipient_contact, member_id, password], daemon=True)
    t.start()


def setup_dirs():
    """
    Creates all the required directories
    """
    dir_list = [
        'assembly_config', 
        'attendance', 
        'baptism_photos',
        'deactivated_assembly',
        'incomplete_reg_acc' + os.sep + 'data',
        'incomplete_reg_acc' + os.sep + 'profile_photos',
        'profile_photos',
        'push_notifications'
    ]
    for dir_path in dir_list:
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], dir_path)
        os.makedirs(full_path, exist_ok=True)