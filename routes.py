from flask import render_template, request, make_response, jsonify, Response
import json
from datetime import datetime
from app import app, db
from models import User, Baptism, RalliesAndConventions, Dedication, Death
import utils


# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/member_datatable')
def member_datatable():
    return render_template('member-datatable.html')

@app.route('/publications')
def publications():
    return render_template('publications.html')

@app.route('/index_2')
def index_2():
    return render_template('birth.html')

@app.route('/birth')
def birth():
    return render_template('birth.html')

@app.route('/view_user')
def view_user():
    return render_template('member-datatable.html')

@app.route('/promotion_and_transfer')
def promotion_and_transfer():
    return render_template('promotion-and-transfer.html')

@app.route('/overview')
def overview():
    return render_template('promotion-and-transfer.html')

@app.route('/messages')
def messages():
    return render_template('baptism-certificates.html')

@app.route('/user')
def user():
    return render_template('baptism-certificates.html')

@app.route('/my_activities')
def my_activities():
    return render_template('baptism-certificates.html')

@app.route('/login_v2')
def login_v2():
    return render_template('baptism-certificates.html')

@app.route('/office_of_the_district_pastor')
def office_of_the_district_pastor():
    return render_template('add-user.html')

@app.route('/office_of_the_district_secretary')
def office_of_the_district_secretary():
    return render_template('add-user.html')

@app.route('/records')
def records():
    return render_template('add-user.html')

@app.route('/admin_emmanuel')
def admin_emmanuel():
    return render_template('add-user.html')

@app.route('/admin_glory')
def admin_glory():
    return render_template('add-user.html')

@app.route('/all_datatables')
def all_datatables():
    return render_template('add-user.html')

@app.route('/admin_hope')
def admin_hope():
    return render_template('baptism-certificates.html')

@app.route('/death')
def death():
    try:
        data_1 = db.session.query(Death, User).join(User).all()
        death_data = []
        for death, user in data_1:
            row_data = {
                "record_id": str(death.id),
                "member_id": death.member_id,
                "full_name": f"{user.last_name}, {user.first_name} {user.other_names if user.other_names else ''}",
                "assembly": user.assembly,
                "ministry": user.ministry,
                "aged": str(death.death_date.year - user.dob.year),
                "date_of_birth": '{}-{}-{}'.format(user.dob.year, user.dob.month, user.dob.day),
                "death_date": '{}-{}-{}'.format(death.death_date.year, death.death_date.month, death.death_date.day),
                "burial_date": '{}-{}-{}'.format(death.burial_date.year, death.burial_date.month, death.burial_date.day),
                "place_of_burial": death.place_of_burial,
                "officiating_minister": death.officiating_minister
            }
            death_data.append(row_data)
        #print(death_data[0])
        return render_template('death.html', death_data=death_data)
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/death_submit', methods=['POST'])
def death_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get("record_id").strip()
        member_id = form.get('member_id')
        death_date = form.get('death_date').strip()
        assembly = form.get("assembly")
        ministry = form.get("ministry")
        date_of_birth = form.get('date_of_birth')
        aged = form.get("aged")
        burial_date = form.get('burial_date').strip()
        place_of_burial = form.get('place_of_burial').strip()
        officiating_minister = form.get('officiating_minister').strip() 

        try:
            if record_id == "":
                # create new baptism object
                death = Death(member_id=member_id, place_of_burial=place_of_burial, officiating_minister=officiating_minister)

                death.set_death_date(death_date)
                death.set_burial_date(burial_date)

                # add the new baptism data to the database and save the changes
                db.session.add(death)
                db.session.commit()
            else: 
                # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
                # https://docs.sqlalchemy.org/en/13/core/dml.html
                member_id = int(member_id)
                row_dict = {
                    "death_date": death_date,
                    "burial_date": burial_date,
                    "place_of_burial": place_of_burial,
                    "officiating_minister": officiating_minister
                }
                Death.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            data = {
            "death_id": utils.get_death_id(),
            "member_id": member_id,
            "date_of_birth": date_of_birth,
            "death_date": death_date,
            "aged": aged,
            'assembly':assembly,
            'ministry':ministry,
            "burial_date": burial_date,
            "place_of_burial": place_of_burial,
            "officiating_minister": officiating_minister
            }

            return Response(json.dumps(data), status=200, mimetype='application/json')

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            #return Response(json.dumps({'status':'OK', 'message': 'successful', 'member_id': member_id}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/send_dedication_notif_msg', methods=['POST'])
def send_dedication_notif_msg():
    try:
        if request.method == 'POST':
            form = request.form
            message_id = form.get('message_id')
            msg_record_id = form.get('msg_cr_id')
            message_body = form.get('message_body')

            msg_data = {
                "message_id": message_id,
                "msg_cr_id": msg_record_id,
                "message_body": message_body
            }

            utils.save_notif_msg(msg_data, 'dedication')

            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Failed to send message'}), status=400, mimetype='application/json')

@app.route('/load_dedication_msg_id', methods=['POST'])
def load_dedication_msg_id():
    try:
        if request.method == 'POST':
            msg_id = utils.get_notif_msg_id(dir_name="dedication")
            return Response(json.dumps({'msg_id': msg_id}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Failed to load Message ID'}), status=400, mimetype='application/json')

@app.route('/dedication')
def dedication():
    try:
        ded_data = Dedication.query.all()
        return render_template('dedication.html', ded_data=ded_data)
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/dedication_submit', methods=['POST'])
def dedication_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get('record_id').strip()
        member_id_father = form.get('member_id_father').strip()
        member_id_mother = form.get('member_id_mother').strip()
        child_name = form.get('child_name').strip()
        child_dob = form.get('child_dob')
        dedication_date_time = form.get('dedication_date_time')
        officiating_minister = form.get('officiating_minister').strip()
        assembly = form.get('assembly')
        place_of_ceremony = form.get('place_of_ceremony').strip()

        try:
            if record_id == "":
                dedication = Dedication(member_id_father=member_id_father, member_id_mother=member_id_mother, child_name=child_name,
                                        officiating_minister=officiating_minister, assembly=assembly, place_of_ceremony=place_of_ceremony)

                dedication.set_child_dob(child_dob)
                dedication.set_dedication_date_time(dedication_date_time)

                db.session.add(dedication)
                db.session.commit()
            else:
                record_id = int(record_id)
                # child_dob = child_dob.split('-')
                # child_dob = datetime(int(child_dob[0]), int(child_dob[1]), int(child_dob[2]))
                row_dict = {
                    "id": record_id,
                    "member_id_father": member_id_father,
                    "member_id_mother": member_id_mother,
                    "child_name": child_name,
                    "officiating_minister": officiating_minister,
                    "assembly": assembly,
                    "place_of_ceremony": place_of_ceremony,
                    "child_dob": child_dob,
                    "dedication_date_time": utils.set_date_time(dedication_date_time)
                }
                Dedication.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            data = {
                "member_id_father": member_id_father,
                "member_id_mother": member_id_mother,
                "child_name": child_name,
                "child_dob": child_dob,
                "dedication_date_time": dedication_date_time,
                "officiating_minister": officiating_minister,
                "assembly": assembly,
                "place_of_ceremony": place_of_ceremony
            }

            return Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/rallies_and_conventions')
def rallies_and_conventions():
    try:
        cr_data = RalliesAndConventions.query.all()
        return render_template('rallies-and-conventions.html', cr_data=cr_data)
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/rallies_and_conventions_submit', methods=['POST'])
def rallies_and_conventions_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        cr_id = form.get("cr_id").strip()
        cr_title = form.get('cr_title')
        cr_type = form.get('cr_type')
        start_date_time = form.get('start_date_time')
        end_date_time = form.get('end_date_time')
        assembly = form.get('assembly')
        venue = form.get('venue').strip()
        souls_won = form.get('souls_won')
        head_count = form.get('head_count')
        mode_of_count = form.get('mode_of_count')

        try:
            if cr_id == "":
                rallies_and_conventions = RalliesAndConventions(cr_type=cr_type, assembly=assembly, venue=venue, souls_won=souls_won, \
                head_count=head_count, mode_of_count=mode_of_count, cr_title=cr_title)

                rallies_and_conventions.set_start_date_time(start_date_time)
                rallies_and_conventions.set_end_date_time(end_date_time)

                db.session.add(rallies_and_conventions)
                db.session.commit()
            else:
                # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
                # https://docs.sqlalchemy.org/en/13/core/dml.html
                cr_id = int(cr_id)
                row_dict = {
                    "cr_type": cr_type,
                    "assembly": assembly,
                    "venue": venue,
                    "souls_won": souls_won,
                    "head_count": head_count,
                    "mode_of_count": mode_of_count,
                    "cr_title": cr_title,
                    "start_date_time": utils.set_date_time(start_date_time),
                    "end_date_time": utils.set_date_time(end_date_time)
                }
                RalliesAndConventions.query.filter_by(cr_id=cr_id).update(row_dict)
                db.session.commit()

            data = {
                "cr_id": utils.get_rc_id(),
                "cr_title": cr_title,
                "cr_type": cr_type,
                "start_date_time": start_date_time,
                "end_date_time": end_date_time,
                "assembly": assembly,
                "venue": venue,
                "souls_won": str(souls_won),
                "head_count": str(head_count),
                "mode_of_count": mode_of_count
            }

            return Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/send_baptism_cert_notif_msg', methods=['POST'])
def send_baptism_cert_notif_msg():
    try:
        if request.method == 'POST':
            form = request.form
            message_id = form.get('message_id')
            msg_record_id = form.get('msg_record_id')
            message_body = form.get('message_body')

            msg_data = {
                "message_id": message_id,
                "msg_record_id": msg_record_id,
                "message_body": message_body
            }

            utils.save_notif_msg(msg_data, 'baptism_certificates')

            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Failed to send message'}), status=400, mimetype='application/json')


@app.route('/load_baptism_cert_msg_id', methods=['POST'])
def load_baptism_cert_msg_id():
    try:
        if request.method == 'POST':
            msg_id = utils.get_notif_msg_id(dir_name="baptism_certificates")
            return Response(json.dumps({'msg_id': msg_id}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Failed to load Message ID'}), status=400, mimetype='application/json')


@app.route('/load_baptism_by_id/<src_id>', methods=['POST'])
def load_baptism_by_id(src_id):
    try:
        if request.method == 'POST':
            member_id = src_id
            return Response(json.dumps(utils.read_baptism_by_member_id(member_id)), status=200, mimetype='application/json')
    except Exception as e:
            print(e)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
        
@app.route('/baptism_certificates')
def baptism_certificates():
     try:
        data_1 = db.session.query(Baptism, User).join(User).all()
        bc_data = []
        for baptism, user in data_1:
            row_data = {
                "record_id": str(baptism.id),
                "member_id": baptism.member_id,
                "full_name": f"{user.last_name}, {user.first_name} {user.other_names if user.other_names else ''}",
                "assembly": user.assembly,
                "date_of_baptism": baptism.get_date_of_baptism(baptism.date_of_baptism),
                "place_of_baptism": baptism.place_of_baptism,
                "officiating_minister": baptism.officiating_minister,
                "district": baptism.district,
                "area": baptism.area,
                "country": baptism.country,
                "certificates": 2 if utils.get_img_path(baptism.member_id) == "" else 1
            }
            bc_data.append(row_data)
        #print(bc_data[0])
        return render_template('baptism-certificates.html', bc_data=bc_data)
     except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/baptism_certificates_submit', methods=['POST'])
def baptism_certificates_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get("record_id").strip()
        member_id = form.get('member_id')
        date_of_baptism = form.get('date_of_baptism').strip()
        place_of_baptism = form.get('place_of_baptism').strip()
        officiating_minister = form.get('officiating_minister').strip() 
        district = form.get('district')
        area = form.get('area').strip()
        country = form.get('country').strip()

        try:
            if record_id == "":
                if not utils.upload_baptism_photo(member_id):
                    return Response(json.dumps({'status':'FAIL', 'message': 'Image error. Invalid photo.'}), status=400, mimetype='application/json')
                # create new baptism object
                baptism = Baptism(member_id=member_id, place_of_baptism=place_of_baptism, officiating_minister=officiating_minister, \
                    district=district, area=area, country=country)
                baptism.set_date_of_baptism(date_of_baptism)

                # add the new baptism data to the database and save the changes
                db.session.add(baptism)
                db.session.commit()
            else: 
                # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
                # https://docs.sqlalchemy.org/en/13/core/dml.html
                member_id = int(member_id)
                row_dict = {
                    "date_of_baptism": date_of_baptism,
                    "place_of_baptism": place_of_baptism,
                    "officiating_minister": officiating_minister,
                    "district": district,
                    "area": area,
                    "country": country
                }
                Baptism.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful', 'member_id': member_id}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
        

@app.route('/load_user_by_id/<src_id>', methods=['POST'])
def load_user_by_id(src_id):
    try:
        if request.method == 'POST':
            member_id = request.form.get(src_id).strip()           
            return Response(json.dumps(utils.read_user_by_member_id(member_id)), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/load_user_img/<member_id>', methods=['POST'])
def load_user_img(member_id):
    try:
        if request.method == 'POST':        
            return Response(json.dumps({"img": utils.get_img_path(member_id)}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Failed to load profile photo'}), status=400, mimetype='application/json')

@app.route('/add_user')
def add_user():
    return render_template('add-user.html')    

@app.route('/add_user_submit', methods=['POST'])
def add_user_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        # member_id = form.get('member_id')
        first_name = form.get('first_name').strip()
        last_name = form.get('last_name').strip()
        other_names = form.get('other_names').strip() 
        gender = form.get('gender')
        occupation = form.get('occupation').strip()
        contact_phone_1 = form.get('contact_phone_1').strip()
        contact_phone_2 = form.get('contact_phone_2').strip()
        dob = form.get('dob')
        email = form.get('email').strip()
        marital_status = form.get('marital_status')
        assembly = form.get('assembly')
        ministry = form.getlist('ministry')
        group = form.get('group')

        password = form.get('password')
        comm_email = form.get('comm_email')
        comm_sms = form.get('comm_sms')
        comm_phone = form.get('comm_phone')
        
        address_line_1 = form.get('address_line_1').strip()
        address_line_2 = form.get('address_line_2').strip()
        digital_address_code = form.get('digital_address_code').strip()
        region = form.get('region').strip()
        district = form.get('district').strip()
        country = form.get('country')

        try:
            member_id = utils.gen_id(assembly, ministry)
            if not member_id:
                return Response(json.dumps({'status':'FAIL', 'message': 'Invalid combination of ministries.'}), status=400, mimetype='application/json')
            if not utils.upload_profile_photo(member_id):
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

            # send confirmation email or sms
            if email:
                subject = "COP"
                msg_content = utils.compose_email_msg(member_id, password)
                utils.send_email(subject, email, msg_content)
            else:
                msg = utils.compose_sms_msg(member_id, password)
                utils.send_sms(msg, contact_phone_1)

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful', 'member_id': member_id}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route("/add_user_save_continue", methods=['POST'])
def add_user_save_continue():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        first_name = form.get('first_name').strip()
        last_name = form.get('last_name').strip()
        other_names = form.get('other_names').strip() 
        gender = form.get('gender')
        occupation = form.get('occupation').strip()
        contact_phone_1 = form.get('contact_phone_1').strip()
        contact_phone_2 = form.get('contact_phone_2').strip()
        dob = form.get('dob')
        email = form.get('email').strip()
        marital_status = form.get('marital_status')
        assembly = form.get('assembly')
        ministry = form.getlist('ministry')
        group = form.get('group')

        password = form.get('password')
        comm_email = form.get('comm_email')
        comm_sms = form.get('comm_sms')
        comm_phone = form.get('comm_phone')
        
        address_line_1 = form.get('address_line_1').strip()
        address_line_2 = form.get('address_line_2').strip()
        digital_address_code = form.get('digital_address_code').strip()
        region = form.get('region').strip()
        district = form.get('district').strip()
        country = form.get('country')
        
        try:
            # generate the pseudo id
            pseudo_member_id = utils.gen_pseudo_id(first_name, last_name, contact_phone_1)
            # put the data in a dictionary
            data = {
                "member_id": pseudo_member_id,
                "first_name": first_name,
                "last_name": last_name,
                "other_names": other_names,
                "gender": gender,
                "occupation": occupation,
                "contact_phone_1": contact_phone_1,
                "contact_phone_2": contact_phone_2,
                "dob": dob,
                "email": email,
                "marital_status": marital_status,
                "assembly": assembly,
                "ministry": ",".join(ministry),
                "group": group,
                "password": password,
                "comm_email": comm_email,
                "comm_sms": comm_sms,
                "comm_phone": comm_phone,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "digital_address_code": digital_address_code,
                "region": region,
                "district": district,
                "country": country
            }
            # save the data
            utils.save_incomplete_reg(data)

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Failed to save!'}), status=400, mimetype='application/json')


@app.route("/add_user_save_new", methods=['POST'])
def add_user_save_new():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        first_name = form.get('first_name').strip()
        last_name = form.get('last_name').strip()
        other_names = form.get('other_names').strip() 
        gender = form.get('gender')
        occupation = form.get('occupation').strip()
        contact_phone_1 = form.get('contact_phone_1').strip()
        contact_phone_2 = form.get('contact_phone_2').strip()
        dob = form.get('dob')
        email = form.get('email').strip()
        marital_status = form.get('marital_status')
        assembly = form.get('assembly')
        ministry = form.getlist('ministry')
        group = form.get('group')

        password = form.get('password')
        comm_email = form.get('comm_email')
        comm_sms = form.get('comm_sms')
        comm_phone = form.get('comm_phone')
        
        address_line_1 = form.get('address_line_1').strip()
        address_line_2 = form.get('address_line_2').strip()
        digital_address_code = form.get('digital_address_code').strip()
        region = form.get('region').strip()
        district = form.get('district').strip()
        country = form.get('country')
        
        try:
            # generate the pseudo id
            pseudo_member_id = utils.gen_pseudo_id(first_name, last_name, contact_phone_1)
            # put the data in a dictionary
            data = {
                "member_id": pseudo_member_id,
                "first_name": first_name,
                "last_name": last_name,
                "other_names": other_names,
                "gender": gender,
                "occupation": occupation,
                "contact_phone_1": contact_phone_1,
                "contact_phone_2": contact_phone_2,
                "dob": dob,
                "email": email,
                "marital_status": marital_status,
                "assembly": assembly,
                "ministry": ",".join(ministry),
                "group": group,
                "password": password,
                "comm_email": comm_email,
                "comm_sms": comm_sms,
                "comm_phone": comm_phone,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "digital_address_code": digital_address_code,
                "region": region,
                "district": district,
                "country": country
            }
            # save the data
            utils.save_incomplete_reg(data)

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Failed to save!'}), status=400, mimetype='application/json')


@app.route("/add_user_save_exit", methods=['POST'])
def add_user_save_exit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        first_name = form.get('first_name').strip()
        last_name = form.get('last_name').strip()
        other_names = form.get('other_names').strip() 
        gender = form.get('gender')
        occupation = form.get('occupation').strip()
        contact_phone_1 = form.get('contact_phone_1').strip()
        contact_phone_2 = form.get('contact_phone_2').strip()
        dob = form.get('dob')
        email = form.get('email').strip()
        marital_status = form.get('marital_status')
        assembly = form.get('assembly')
        ministry = form.getlist('ministry')
        group = form.get('group')

        password = form.get('password')
        comm_email = form.get('comm_email')
        comm_sms = form.get('comm_sms')
        comm_phone = form.get('comm_phone')
        
        address_line_1 = form.get('address_line_1').strip()
        address_line_2 = form.get('address_line_2').strip()
        digital_address_code = form.get('digital_address_code').strip()
        region = form.get('region').strip()
        district = form.get('district').strip()
        country = form.get('country')
        
        try:
            # generate the pseudo id
            pseudo_member_id = utils.gen_pseudo_id(first_name, last_name, contact_phone_1)
            # put the data in a dictionary
            data = {
                "member_id": pseudo_member_id,
                "first_name": first_name,
                "last_name": last_name,
                "other_names": other_names,
                "gender": gender,
                "occupation": occupation,
                "contact_phone_1": contact_phone_1,
                "contact_phone_2": contact_phone_2,
                "dob": dob,
                "email": email,
                "marital_status": marital_status,
                "assembly": assembly,
                "ministry": ",".join(ministry),
                "group": group,
                "password": password,
                "comm_email": comm_email,
                "comm_sms": comm_sms,
                "comm_phone": comm_phone,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "digital_address_code": digital_address_code,
                "region": region,
                "district": district,
                "country": country
            }
            # save the data
            utils.save_incomplete_reg(data)

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Failed to save!'}), status=400, mimetype='application/json')