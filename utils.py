from app import db
from models import User


def check_email_duplicates(email):
    ret = User.query.filter_by(email=email).first()
    return (False if ret is None else True)

def check_contact_duplicates(contact):
    ret = User.query.filter_by(contact_phone_1=contact).first()
    return (False if ret is None else True)

# 8-digit code
# 1st digit: Assembly (1=Emmanuel, 2=Glory, 3=Hope)
# 2nd - 6th: Position of registration
# 7th - 8th: Ministries
#
def gen_id(church_affiliation):
    assemblies = ["EEA", "GA", "HA"]
    ministries = ["CM", "EM", "PM", "WM", "YM"]
    eea_bible_groups = ["EAG", "EPG", "EJG", "ELG"]
    glory_bible_groups = ["GAGO", "GAGW", "GAGT", "GAGF"]
    hope_bible_groups = ["HAGO", "HAGW", "HAGT", "HAGF"]

    valid_ministries = ['C', 'E', 'EP', 'EPY', 'EW', 'EWY', 'EY', 'P', 'PY', 'W', 'WY', 'Y']

    member_id = ""
    assembly = ""
    # append assemblies value
    for i, aff in assemblies:
        if church_affiliation.__contains__(aff):
            assembly = assemblies[i]
            break
    # append the 2nd to 6th values
    User.query.filter(User.church_affiliation.startswith(assembly))
    

