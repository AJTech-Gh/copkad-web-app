from flask import render_template, request, make_response, jsonify, Response
import json
from app import app, db
from models import User

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
        photo_id = form.get('photo_id')
        member_id = form.get('member_id')
        first_name = form.get('first_name')
        last_name = form.get('last_name')
        other_names = form.get('other_names') 
        gender = form.get('gender')
        occupation = form.get('occupation')
        contact_one = form.get('contact_one')
        contact_two = form.get('contacta_two')
        dob = form.get('dob')
        email = form.get('email')
        marital_status = form.get('marital_status')
        church_affiliation = form.get('church_affiliation')

        password = form.get('password')
        mode_of_communication = form.get('mode_of_communication')
        
        address_line_one = form.get('address_line_one')
        address_line_two = form.get('address_line_two')
        digital_address = form.get('digital_address')
        region = form.get('region')
        district = form.get('district')
        country = form.get('country')

        # create new user object
        user = User(photo_id=photo_id, member_id=member_id, first_name=first_name, last_name=last_name, other_names=other_names,\
                    gender=gender, occupation=occupation, contact_one=contact_one, contact_two=contact_two, dob=dob, email=email, \
                    marital_status=marital_status, church_affiliation=church_affiliation, address_line_one=address_line_one, \
                    address_line_two=address_line_two, digital_address=digital_address, region=region, district=district, country=country
                )
        user.set_password(password)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()
        # return the success response to Ajax
        # return json.dumps({'status':'OK', 'message': 'successful'})
        return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')

    
    


