from flask import render_template, request, make_response, jsonify, Response
import json
from datetime import datetime
from app import app, db
from models import User
import utils


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_user')
def add_user():
    return render_template('add-user.html')

@app.route('/member_datatable')
def member_datatable():
    return render_template('member-datatable.html')

@app.route('/publications')
def publications():
    return render_template('member-datatable.html')

@app.route('/index_2')
def index_2():
    return render_template('member-datatable.html')

@app.route('/view_user')
def view_user():
    return render_template('member-datatable.html')

@app.route('/user')
def user():
    return render_template('member-datatable.html')

@app.route('/office_of_the_district_pastor')
def office_of_the_district_pastor():
    return render_template('add-user.html')

@app.route('/office_of_the_district_secretary')
def office_of_the_district_secretary():
    return render_template('add-user.html')

@app.route('/records')
def records():
    return render_template('add-user.html')

@app.route('/add_user_submit', methods=['POST'])
def add_user_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        # member_id = form.get('member_id')
        first_name = form.get('first_name')
        last_name = form.get('last_name')
        other_names = form.get('other_names') 
        gender = form.get('gender')
        occupation = form.get('occupation')
        contact_phone_1 = form.get('contact_phone_1')
        contact_phone_2 = form.get('contact_phone_2')
        dob = form.get('dob')
        email = form.get('email')
        marital_status = form.get('marital_status')
        assembly = form.get('assembly')
        ministry = form.getlist('ministry')
        group = form.get('group')

        password = form.get('password')
        comm_email = form.get('comm_email')
        comm_sms = form.get('comm_sms')
        comm_phone = form.get('comm_phone')
        
        address_line_1 = form.get('address_line_1')
        address_line_2 = form.get('address_line_2')
        digital_address_code = form.get('digital_address_code')
        region = form.get('region')
        district = form.get('district')
        country = form.get('country')

        try:
            member_id = utils.gen_id(assembly, ministry)
            if not member_id:
                return Response(json.dumps({'status':'FAIL', 'message': 'Invalid combination of ministries.'}), status=400, mimetype='application/json')
            if not utils.upload_photo(member_id):
                return Response(json.dumps({'status':'FAIL', 'message': 'Image error. Invalid photo.'}), status=400, mimetype='application/json')
            if utils.check_email_duplicates(email):
                return Response(json.dumps({'status':'FAIL', 'message': 'Email already exists.'}), status=400, mimetype='application/json')
            if utils.check_contact_duplicates(contact_phone_1):
                return Response(json.dumps({'status':'FAIL', 'message': 'Contact 1 already exists.'}), status=400, mimetype='application/json')
            # create new user object
            user = User(member_id=member_id, first_name=first_name, last_name=last_name, other_names=other_names,
                        occupation=occupation, email=email, marital_status=marital_status, assembly=assembly,
                        address_line_1=address_line_1, address_line_2=address_line_2, digital_address_code=digital_address_code, region=region, 
                        district=district, country=country
                    )
            user.set_gender(gender)
            user.set_contact_phone_1(contact_phone_1)
            user.set_contact_phone_2(contact_phone_2)
            user.set_dob(dob)
            user.set_ministry(ministry)
            user.set_group(group)
            user.set_password(password)
            user.set_comm_email(comm_email)
            user.set_comm_sms(comm_sms)
            user.set_comm_phone(comm_phone)
            # add the new user to the database and save the changes
            db.session.add(user)
            db.session.commit()
            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
        except Exception as e:
            # print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


