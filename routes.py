from flask import render_template, request, make_response, jsonify, Response
from flask.signals import request_started
from flask_login import current_user, login_user, logout_user, login_required
import json, os, re
from datetime import datetime
from flask.helpers import url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from app import app, db, login_manager
from models import User, Baptism, RalliesAndConventions, Dedication, Death, Promotion, Transfer, Birth, Accessibility
import utils
from constants import *


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

@app.route('/publications')
def publications():
    return render_template('publications.html')

@app.route('/index_2')
def index_2():
    return render_template('birth.html')

@app.route('/view_user')
def view_user():
    return render_template('member-datatable.html')

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

@app.route('/messaging')
def messaging():
    return render_template('messaging.html')

@app.route('/finance_info')
def finance_info():
    return render_template('finance-info.html')

@app.route('/office_of_the_district_pastor')
def office_of_the_district_pastor():
    return render_template('add-user.html')

@app.route('/office_of_the_district_secretary')
def office_of_the_district_secretary():
    return render_template('add-user.html')

@app.route('/records')
def records():
    return render_template('report.html')

@app.route('/admin_emmanuel')
def admin_emmanuel():
    return render_template('add-user.html')

@app.route('/admin_glory')
def admin_glory():
    return render_template('add-user.html')

@app.route('/admin_hope')
def admin_hope():
    return render_template('print-out-sample.html')

@app.route('/all_datatables')
def all_datatables():
    return render_template('add-user.html')


@app.route('/personal_information')
def personal_information():
    return render_template('personal-information.html')

@app.route('/account_information')
def account_information():
    return render_template('account-information.html')

@app.route('/financial_status')
def financial_status():
    return render_template('financial-status.html')

@app.route('/change_password')
def change_password():
    return render_template('change-password.html')

@app.route('/admin_pledges_overview')
def admin_pledges_overview():
    return render_template('personal-information.html')

@app.route('/reports')
def reports():
    return render_template('report.html')

@app.route('/transfers_and_promotions')
def transfers_and_promotions():
    return render_template('report.html')

@app.route('/new_converts')
def new_converts():
    return render_template('report.html')

@app.route('/holyghost_baptism')
def holyghost_baptism():
    return render_template('report.html')

@app.route('/general_finance')
def general_finance():
    return render_template('report.html')

@app.route('/tithes')
def tithes():
    return render_template('report.html')

@app.route('/missions_offering')
def missions_offering():
    return render_template('report.html')

@app.route('/daily_offering')
def daily_offering():
    return render_template('report.html')

@app.route('/welfare')
def welfare():
    return render_template('report.html')

@app.route('/donations')
def donations():
    return render_template('report.html')

@app.route('/books_stationary')
def books_stationary():
    return render_template('report.html')

@app.route('/donations_out')
def donations_out():
    return render_template('report.html')

@app.route('/other_expenditure')
def other_expenditure():
    return render_template('report.html')

@app.route('/pledges')
def pledges():
    return render_template('report.html')

@app.route('/special_offering')
def special_offering():
    return render_template('report.html')

@app.route('/utility_expense')
def utility_expense():
    return render_template('report.html')

@app.route('/wages_salaries')
def wages_salaries():
    return render_template('report.html')

@app.route('/member_dashboard')
def member_dashboard():
    return render_template('report.html')

@app.route('/bible_studies_group')
def bible_studies_group():
    return render_template('report.html')


@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/login')
def login():
    if current_user.is_authenticated:
        if str(current_user).split(':')[0].lower() == 'accessibility':
            permission = current_user.permission
            if permission == 'super_admin':
                return redirect(url_for('admin_dashboard'))
            if permission.startswith('admin'):
                return redirect(url_for('overview'))
            if permission.startswith('chief'):
                return redirect(url_for('finance_info'))
            if permission.startswith('finance'):
                return redirect(url_for('finance_info'))
        else:
            return redirect(url_for('personal_information'))
    return render_template('login.html')

@app.route('/login_submit', methods=['GET', 'POST'])
def login_submit():
    try:
        if request.method == 'GET':
            next_param = request.args.get('next')
            if utils.valid_next_param(next_param):
                return redirect(url_for('login'))
        if request.method == 'POST':
            if current_user.is_authenticated:
                if str(current_user).split(':')[0].lower() == 'accessibility':
                    permission = current_user.permission
                    if permission == 'super_admin':
                        return Response(json.dumps({'status': 'SUCCESS', 'url': ' '}), status=200, mimetype='application/json')
                    if permission.startswith('admin'):
                        return Response(json.dumps({'status': 'SUCCESS', 'url': 'overview'}), status=200, mimetype='application/json')
                    if permission.startswith('chief'):
                        return Response(json.dumps({'status': 'SUCCESS', 'url': 'finance_info'}), status=200, mimetype='application/json')
                    if permission.startswith('finance'):
                        return Response(json.dumps({'status': 'SUCCESS', 'url': 'finance_info'}), status=200, mimetype='application/json')
                else:
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'personal_information'}), status=200, mimetype='application/json')
            else:
                # get the form data
                form = request.form
                username = form.get('username')
                password = form.get('password')
                remember = form.get('remember')
                # login the user
                admin = Accessibility.query.filter_by(permission=username).first()
                # if the credentials doesn't match any admin, check the user's table
                if admin is None or not admin.check_password(password):
                    # login as user else return to login screen
                    user = User.query.filter_by(member_id=username).first()
                    if user is None or not user.check_password(password):
                        return Response(json.dumps({'status': 'FAIL', 'message': 'Login failed'}), status=400, mimetype='application/json') #redirect(url_for('login'))
                    login_user(user, remember=remember)
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'personal_information'}), status=200, mimetype='application/json')
                # login as the appropriate admin
                permission = admin.permission
                login_user(admin, remember=remember)
                if permission == 'super_admin':
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'admin_dashboard'}), status=200, mimetype='application/json')
                if permission.startswith('admin'):
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'overview'}), status=200, mimetype='application/json')
                if permission.startswith('chief'):
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'finance_info'}), status=200, mimetype='application/json')
                if permission.startswith('finance'):
                    return Response(json.dumps({'status': 'SUCCESS', 'url': 'finance_info'}), status=200, mimetype='application/json')
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
    

@app.route('/view_accessibility/<member_id>', methods=['POST'])
def view_accessibility(member_id):
    try:
        user_data = utils.read_user_by_member_id(member_id)
        accessibility_data = utils.read_accessibility_by_member_id(member_id)
        return Response(json.dumps({'status': 'SUCCESS', 'user_data': user_data, 'view_accessibility_data': accessibility_data}), status=200, mimetype='application/json') 
    except Exception as e:
        print(e)
        # print(form)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/remove_accessibility/<member_id>', methods=['POST'])
def remove_accessibility(member_id):
    try:
        utils.remove_access(member_id)
        return Response(json.dumps({'status': 'SUCCESS', 'message': f'{member_id}\'s privileges has been removed '}), status=200, mimetype='application/json') 
    except Exception as e:
        print(e)
        # print(form)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/accessibility_submit', methods=['POST'])
def accessibility_submit():
    form = request.form
    member_id = form.get('member_id').strip()
    permission = form.get('permission')
    assembly = form.get('assembly')
    assembly_status = form.get('assembly_status')
    accessibility_password = utils.generate_password()
    assigned_assembly = ' '.join([p.capitalize().strip() for p in permission.split('_')[1:]]) + ' Assembly'
    try:
        #get the form data transmitted by Ajax
        #form is an ImmutableMultiDict object
        #https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        exceptions = ['chief', 'super']
        if  not exceptions.__contains__(permission.split('_')[0]) and User.query.filter_by(member_id=member_id, assembly=assigned_assembly).count() == 0: 
            return Response(json.dumps({'status':'FAIL', 'message': f'{member_id} is not a member of {assigned_assembly}'}), status=400, mimetype='application/json')

        if Accessibility.query.filter_by(permission=permission).count() == 0:
            new_access = Accessibility(member_id=member_id, assembly=assembly, permission=permission, assembly_status=assembly_status)
            new_access.set_password(accessibility_password)
            db.session.add(new_access)
            db.session.commit()
        else:
            member_id = member_id
            row_dict = {
                "member_id": member_id,
                "password_hash": generate_password_hash(accessibility_password),
                "assembly": assembly,
                "permission": permission,
                "assembly_status": assembly_status
            }
            Accessibility.query.filter_by(permission=permission).update(row_dict)
            db.session.commit()

        # data = {
        #     "member_id": member_id,
        #     "password": password,
        #     "assembly_name": assembly_name,
        #     "permission": permission,
        #     "assembly_status": assembly_status
        # }

        return Response(json.dumps({'status': 'SUCCESS', 'message': f'Access granted successfully'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        # print(form)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

    

@app.route('/activate_assembly/<assembly_name>', methods=['POST'])
def activate_assembly(assembly_name):
    try:
        assembly_name_original = ' '.join([p.capitalize() for p in assembly_name.split('_')])
        if not utils.activate_assembly(assembly_name):
            return Response(json.dumps({'status':'FAIL', 'message': f'Failed to activate {assembly_name_original}'}), status=400, mimetype='application/json')
        return Response(json.dumps({'status': 'SUCCESS', 'message': f'{assembly_name_original} activated successfully'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/deactivate_assembly/<assembly_name>', methods=['POST'])
def deactivate_assembly(assembly_name):
    try:
        assembly_name_original = ' '.join([p.capitalize() for p in assembly_name.split('_')])
        if not utils.deactivate_assembly(assembly_name):
            return Response(json.dumps({'status':'FAIL', 'message': f'Failed to deactivate {assembly_name_original}'}), status=400, mimetype='application/json')
        return Response(json.dumps({'status': 'SUCCESS', 'message': f'{assembly_name_original} deactivated successfully'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/assembly_forecast/<assembly_name>', methods=['POST'])
def assembly_forecast(assembly_name):
    try:
        assembly_name = ' '.join([p.capitalize() for p in assembly_name.split('_')])
        member_count = str(User.query.filter_by(assembly=assembly_name).count())
        return Response(json.dumps({
            'status':'SUCCESS', 
            'member_count': member_count, 
            'status': {'active': '0', 'inactive': '0', 'backslider': '0'}, 
            'finance': {'income': '0.00', 'expenditure': '0.00'},
            'welfare': '0.00'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/filtered_member_datatable')
def filtered_member_datatable():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission == 'super_admin':
                    message_count = str(utils.get_notif_count())
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    assembly_name = request.args.get("assembly_name")
                    assembly_name_list = assembly_name.split('_')
                    assembly_name = ' '.join([p.capitalize() for p in assembly_name_list])
                    data_1 = User.query.filter_by(assembly=assembly_name).all()
                    data_2 = utils.load_all_incomplete_reg()

                    member_data = []

                    for user in data_1:
                        row_data = {
                            'member_id': user.member_id,
                            'full_name': f'{user.last_name}, {user.first_name} {user.other_names}',
                            'gender': user.gender, 
                            'assembly': user.assembly, 
                            'contact': (f'{user.contact_phone_1}' if user.contact_phone_2.strip() == "" else f'{user.contact_phone_1}/{user.contact_phone_2}'), 
                            'marital_status': user.marital_status.capitalize(), 
                            'ministry': user.ministry, 
                            'status': "1"
                        }
                        member_data.append(row_data)

                    for user in data_2:
                        row_data = {
                            'member_id': user["member_id"],
                            'full_name': f'{user["last_name"]}, {user["first_name"]} {user["other_names"]}',
                            'gender': user['gender'], 
                            'assembly': ("" if user["assembly"] == None else user["assembly"]), 
                            'contact': (f'{user["contact_phone_1"]}' if user["contact_phone_2"].strip() == "" else f'{user["contact_phone_1"]}/{user["contact_phone_2"]}'), 
                            'marital_status': user["marital_status"].capitalize(), 
                            'ministry': user["ministry"], 
                            'status': "0"
                        }
                        member_data.append(row_data)

                    #print(death_data[0])
                    
                    return render_template('member-datatable.html', member_data=member_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission == 'super_admin':
                    message_count = str(utils.get_notif_count())
                    assembly_names, _, _ = utils.load_assembly_data()
                    registered_member_data = utils.assemblies_registration_summary()
                    attendance_notifs = utils.get_attendance_notifs('%')
                    assembly_ui_data = utils.get_assembly_ui_data()
                    access_admin_data = db.session.query(Accessibility, User).join(User).all()

                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)
                    
                    accessibility_list = []
                    for access, user in access_admin_data:
                        admin_data = dict()
                        admin_data['member_id'] = user.member_id
                        admin_data['name'] = f'{user.last_name}, {user.first_name} {user.other_names}' 
                        admin_data['img'] = utils.get_img_path(user.member_id)
                        admin_data['assembly'] = user.assembly
                        admin_data['permission'] = access.permission
                        accessibility_list.append(admin_data)
                    return render_template('admin.html', accessibility_list=accessibility_list, assembly_names=assembly_names, 
                    registered_member_data=registered_member_data, attendance_notifs=attendance_notifs, assembly_ui_data=assembly_ui_data, 
                    permission_map=utils.PERMISSION_MAP, logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img,
                    message_count=message_count
                    )
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/statistical_updates')
def statistical_updates():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin'):
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    stats_data = utils.get_statistical_updates(current_user.assembly)
                    return render_template('statistical-updates.html', stats_data=stats_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img)
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/overview')
@login_required
def overview():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin'):
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)
                    underscored_assembly_name = current_user.assembly.lower().replace(' ', '_')
                    latest_updates = utils.get_latest_updates(underscored_assembly_name)
                    attendance_notifs = utils.get_attendance_notifs(current_user.assembly)
                    return render_template('overview.html', latest_updates=latest_updates, attendance_notifs=attendance_notifs, 
                    logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/upload_attendance', methods=['POST'])
def upload_attendance():
    try:
        form = request.form
        assembly_name = form.get('assembly')
        ret_val = utils.upload_attendance(assembly_name)
        if ret_val == NO_FILE_ERROR:
            return Response(json.dumps({'status':'FAIL', 'message': 'No attendance file selected.'}), status=400, mimetype='application/json')
        elif ret_val == INVALID_FORMAT_ERROR:
            return Response(json.dumps({'status':'FAIL', 'message': 'Invalid file format. Choose a .csv file'}), status=400, mimetype='application/json')
        elif ret_val == FATAL_ERROR:
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
        else:
            pass
        return Response(json.dumps({'status':'SUCCESS', 'message': 'Attendance uploaded successfully'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/view_member_data')
def view_member_data():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    member_id = request.args.get("id")
                    status = request.args.get("status")
                    user_data = {}
                    if status == '0':
                        user_data = utils.read_incomplete_reg(member_id)
                    else:
                        user_data = utils.read_user_by_member_id(member_id)

                    assembly_names, ministry_names, group_names = utils.load_assembly_data()
                    return render_template("add-user.html", user_data=user_data, assembly_names=assembly_names, ministry_names=ministry_names, 
                    group_names=group_names, logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/member_datatable')
def member_datatable():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    data_1 = None
                    if permission == 'super_admin':
                        data_1 = User.query.all()
                    else:
                        data_1 = User.query.filter_by(assembly=current_user.assembly).all()
                    data_2 = utils.load_all_incomplete_reg()

                    member_data = []

                    for user in data_1:
                        row_data = {
                            'member_id': user.member_id,
                            'full_name': f'{user.last_name}, {user.first_name} {user.other_names}',
                            'gender': user.gender, 
                            'assembly': user.assembly, 
                            'contact': (f'{user.contact_phone_1}' if user.contact_phone_2.strip() == "" else f'{user.contact_phone_1}/{user.contact_phone_2}'), 
                            'marital_status': user.marital_status.capitalize(), 
                            'ministry': user.ministry, 
                            'status': "1"
                        }
                        member_data.append(row_data)

                    for user in data_2:
                        row_data = {
                            'member_id': user["member_id"],
                            'full_name': f'{user["last_name"]}, {user["first_name"]} {user["other_names"]}',
                            'gender': user['gender'], 
                            'assembly': ("" if user["assembly"] == None else user["assembly"]), 
                            'contact': (f'{user["contact_phone_1"]}' if user["contact_phone_2"].strip() == "" else f'{user["contact_phone_1"]}/{user["contact_phone_2"]}'), 
                            'marital_status': user["marital_status"].capitalize(), 
                            'ministry': user["ministry"], 
                            'status': "0"
                        }
                        member_data.append(row_data)

                    #print(death_data[0])
                    return render_template('member-datatable.html', member_data=member_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route('/edit_settings')
def edit_settings():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission == 'super_admin':
                    assembly_name = request.args.get('assembly_name')
                    print
                    message_count = str(utils.get_notif_count())
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)
                    
                    assembly_data = utils.read_assembly_config(assembly_name)
                    # print(assembly_data)
                    return render_template('edit-settings.html', assembly_data=assembly_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/settings')
def settings():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission == 'super_admin':
                    message_count = str(utils.get_notif_count())
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)
                    return render_template('settings.html', logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/settings_submit', methods=['POST'])
def settings_submit():
    try:
        form = dict(request.form)

        multi_item_list = ['ministry', 'group', "name_of_offering"]
        offering_items = ['name_of_offering', 'type_of_offering', 'percentage_deduction', 'offering_code']
        no_symbol_assembly_name = re.sub(r'[^\w\s]+', '', form.get('assembly_name'))
        capitalized_assembly_name = ' '.join([p.capitalize().strip() for p in no_symbol_assembly_name.strip().split(' ')])
        config_dict = dict({
            'church_name':form.get('church_name'),
            'assembly_name':capitalized_assembly_name,
            'district_name':form.get('district_name'),
            'area_name':form.get('area_name'),
            'address_line_1':form.get('address_line_1'),
            'address_line_2':form.get('address_line_2'),
            'region':form.get('region'),
            'country':form.get('country'),
            'contact':form.get('contact'),
            'email':form.get('email'),
            'e_password':form.get('e_password')
        })
        
        offering_count = 0
        for item in multi_item_list:
            if item == 'name_of_offering':
                for key in form.keys():
                    if key.__contains__(item):
                        offering_count += 1
                continue
            config_dict[item] = []
            for key in form.keys():
                if key.__contains__(item):
                    config_dict[item].append(form[key])
        
        for i in range(offering_count):
            offering_key = 'offering_' + str(i)
            config_dict[offering_key] = dict()
            for item in offering_items:
                config_dict[offering_key][item] = form[f'[{i}][{item}]']

        utils.save_assembly_config(config_dict)

        if utils.upload_assembly_config_files(capitalized_assembly_name):
            return Response(json.dumps({'status':'FAIL', 'message': 'Could not upload all files'}), status=400, mimetype='application/json')
        # print(config_dict)
        return Response(json.dumps({'status':'SUCCESS', 'message': 'Settings saved successfully'}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
        

@app.route('/births')
def births():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    assembly_names, _, _ = utils.load_assembly_data()
                    if permission == 'super_admin':
                        birth_data = Birth.query.all()
                    else:
                        birth_data = Birth.query.filter_by(assembly=current_user.assembly).all()

                    user_data = User.query.with_entities(User.member_id, User.first_name, User.last_name, User.other_names).all()
                    user_data_dict = {"": ""}
                    # print(user_data)
                    for user in user_data:
                        user_data_dict[user[0]] = f"{user.last_name}, {user.first_name} {user.other_names}"

                    return render_template('birth.html', birth_data=birth_data, user_data_dict=user_data_dict,assembly_names=assembly_names, 
                    logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/birth_submit', methods=['POST'])
def birth_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get('record_id').strip()
        member_id_father = form.get('member_id_father').strip()
        member_id_mother = form.get('member_id_mother').strip()
        father_name = form.get('father_name').strip()
        mother_name = form.get('mother_name').strip()
        child_name = form.get('child_name').strip()
        child_dob = form.get('child_dob')
        ceremony_date_time = form.get('ceremony_date')
        officiating_minister = form.get('officiating_minister').strip()
        assembly = form.get('assembly')

        try:
            if record_id == "":
                new_birth = Birth(member_id_father=member_id_father, member_id_mother=member_id_mother, child_name=child_name,
                                        officiating_minister=officiating_minister, assembly=assembly)

                new_birth.set_child_dob(child_dob)
                new_birth.set_ceremony_date_time(ceremony_date_time)

                db.session.add(new_birth)
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
                    "child_dob": child_dob,
                    "ceremony_date_time": utils.set_ceremony_date_time(ceremony_date_time)
                }
                Birth.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            data = {
                "member_id_father": member_id_father,
                "member_id_mother": member_id_mother,
                "mother_name": mother_name,
                "father_name": father_name,
                "child_name": child_name,
                "child_dob": child_dob,
                "ceremony_date_time": ceremony_date_time,
                "officiating_minister": officiating_minister,
                "assembly": assembly,
            }

            return Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')



@app.route('/promotion_and_transfer')
def promotion_and_transfer():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    data_1 = db.session.query(Promotion, User).join(User).all()
                    promotion_data = []
                    for promotion, user in data_1:
                        if permission == 'super_admin' or current_user.assembly == user.assembly:
                            row_data = {
                                "record_id": str(promotion.id),
                                "member_id": promotion.member_id,
                                "full_name": f"{user.last_name}, {user.first_name} {user.other_names if user.other_names else ''}",
                                "assembly": user.assembly,
                                #"ministry": user.ministry,
                                "age": promotion.age,
                                "present_portfolio": promotion.present_portfolio,
                                "promoted_portfolio": promotion.promoted_portfolio,
                                "portfolio_specification": promotion.portfolio_specification,
                                "promotion_date": '{}-{}-{}'.format(promotion.promotion_date.year, promotion.promotion_date.month, promotion.promotion_date.day),
                                "officiating_minister": promotion.officiating_minister
                            }
                            promotion_data.append(row_data)

                    data_2 = db.session.query(Transfer, User).join(User).all()
                    transfer_data = []
                    for transfer, user in data_2:
                        if permission == 'super_admin' or current_user.assembly == user.assembly:
                            row_data = {
                                "record_id": str(transfer.id),
                                "member_id": transfer.member_id,
                                "full_name": f"{user.last_name}, {user.first_name} {user.other_names if user.other_names else ''}",
                                "assembly": user.assembly,
                                #"ministry": user.ministry,
                                "age": transfer.age,
                                "present_portfolio": transfer.present_portfolio,
                                "transfered_from": transfer.transfered_from,
                                "transfered_to": transfer.transfered_to,
                                "transfer_specification": transfer.transfer_specification,
                                "transfer_date": '{}-{}-{}'.format(transfer.transfer_date.year, transfer.transfer_date.month, transfer.transfer_date.day),
                                "officiating_minister": transfer.officiating_minister
                            }
                            transfer_data.append(row_data)
                    #print(death_data[0])
                    return render_template('promotion-and-transfer.html', promotion_data=promotion_data, transfer_data=transfer_data, 
                    logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/transfer_submit', methods=['POST'])
def transfer_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get("trans_record_id").strip()
        member_id = form.get('trans_member_id')
        full_name = form.get('trans_full_name')
        age = form.get('trans_age').strip()
        assembly = form.get('trans_assembly')
        transfered_from = form.get("trans_transfered_from").strip()
        transfered_to = form.get('trans_transfered_to').strip()
        present_portfolio = form.get("trans_present_portfolio").strip()
        transfer_specification = form.get('trans_specify_transfer').strip()
        transfer_date = form.get('trans_transfer_date')
        officiating_minister = form.get('trans_officiating_minister').strip()

        try:
            # if utils.member_id_exists(member_id, table="promotion"):
            #     return Response(json.dumps({'status':'FAIL', 'message': 'Member ID already exists!'}), status=400, mimetype='application/json')
            if record_id == "":
                # create new transfer object
                transfer = Transfer(member_id=member_id, age=age, present_portfolio=present_portfolio, transfered_from=transfered_from, transfered_to=transfered_to,
                transfer_specification=transfer_specification, officiating_minister=officiating_minister)

                transfer.set_transfer_date(transfer_date)

                # add the new transfer
                # data to the database and save the changes
                db.session.add(transfer)
                db.session.commit()
            else: 
                # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
                # https://docs.sqlalchemy.org/en/13/core/dml.html
                member_id = int(member_id)
                row_dict = {
                    'age':age,
                    'present_portfolio':present_portfolio,
                    'transfered_from':transfered_from,
                    'transfered_to':transfered_to,
                    'transfer_specification':transfer_specification,
                    'transfer_date':transfer_date,
                    'officiating_minister': officiating_minister
                }
                Transfer.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            data = {
            "transfer_id": utils.get_transfer_id(),
            "member_id": member_id,
            "transfer_date": transfer_date,
            "full_name":full_name,
            "age": age,
            "assembly": assembly,
            'present_portfolio':present_portfolio,
            "transfered_from": transfered_from,
            "transfered_to": transfered_to,
            "transfer_specification": transfer_specification,
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


@app.route('/promotion_submit', methods=['POST'])
def promotion_submit():
    if request.method == 'POST':
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get("pro_record_id").strip()
        member_id = form.get('pro_member_id')
        full_name = form.get('pro_full_name')
        age = form.get('pro_age').strip()
        assembly = form.get('pro_assembly')
        present_portfolio = form.get("pro_present_portfolio").strip()
        promoted_portfolio = form.get('pro_promoted_portfolio')
        portfolio_specification = form.get('pro_specify_portfolio').strip()
        promotion_date = form.get('pro_promotion_date')
        officiating_minister = form.get('pro_officiating_minister').strip()

        try:
            # if utils.member_id_exists(member_id, table="promotion"):
            #     return Response(json.dumps({'status':'FAIL', 'message': 'Member ID already exists!'}), status=400, mimetype='application/json')
            if record_id == "":
                # create new transfer object
                promotion = Promotion(member_id=member_id, age=age, present_portfolio=present_portfolio, promoted_portfolio=promoted_portfolio, 
                portfolio_specification=portfolio_specification, officiating_minister=officiating_minister)

                promotion.set_promotion_date(promotion_date)

                # add the new transfer data to the database and save the changes
                db.session.add(promotion)
                db.session.commit()
            else: 
                # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
                # https://docs.sqlalchemy.org/en/13/core/dml.html
                member_id = int(member_id)
                row_dict = {
                    'age':age,
                    'present_portfolio':present_portfolio,
                    'promoted_portfolio':promoted_portfolio,
                    'portfolio_specification':portfolio_specification,
                    'promotion_date':promotion_date,
                    'officiating_minister': officiating_minister
                }
                Promotion.query.filter_by(id=record_id).update(row_dict)
                db.session.commit()

            data = {
            "promotion_id": utils.get_promotion_id(),
            "member_id": member_id,
            "promotion_date": promotion_date,
            "full_name":full_name,
            "age": age,
            "assembly": assembly,
            "present_portfolio":present_portfolio,
            "promoted_portfolio": promoted_portfolio,
            "portfolio_specification": portfolio_specification,
            "officiating_minister": officiating_minister
            }

            return Response(json.dumps(data), status=200, mimetype='application/json')

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            # return Response(json.dumps({'status':'OK', 'message': 'successful', 'member_id': member_id}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/deaths')
def deaths():
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    data_1 = db.session.query(Death, User).join(User).all()
                    death_data = []
                    for death, user in data_1:
                        if permission == 'super_admin' or current_user.assembly == user.assembly:
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
                    return render_template('death.html', death_data=death_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
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
                if utils.member_id_exists(member_id, table="death"):
                    return Response(json.dumps({'status':'FAIL', 'message': 'Member ID already exists!'}), status=400, mimetype='application/json')
                # create new transfer object
                death = Death(member_id=member_id, place_of_burial=place_of_burial, officiating_minister=officiating_minister)

                death.set_death_date(death_date)
                death.set_burial_date(burial_date)

                # add the new transfer data to the database and save the changes
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

            user_data = User.query.filter_by(member_id=member_id).first()
            full_name = user_data.last_name + ', ' + user_data.first_name + ' ' + user_data.other_names
            data = {
            "record_id": record_id,
            "member_id": member_id,
            "full_name": full_name,
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
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    assembly_names, _, _ = utils.load_assembly_data()
                    if permission == 'super_admin':
                        ded_data = Dedication.query.all()
                    else:
                        ded_data = Dedication.query.filter_by(assembly=current_user.assembly)
                    user_data = User.query.with_entities(User.member_id, User.first_name, User.last_name, User.other_names).all()
                    user_data_dict = {"": ""}

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    # print(user_data)
                    for user in user_data:
                        user_data_dict[user[0]] = f"{user.last_name}, {user.first_name} {user.other_names}"

                    return render_template('dedication.html', ded_data=ded_data, user_data_dict=user_data_dict, assembly_names=assembly_names, 
                    logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/dedication_submit', methods=['POST'])
def dedication_submit():
    try:
        # get the form data transmitted by Ajax
        # form is an ImmutableMultiDict object
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
        form = request.form
        record_id = form.get('record_id').strip()
        member_id_father = form.get('member_id_father').strip()
        member_id_mother = form.get('member_id_mother').strip()
        father_name = form.get('father_name').strip()
        mother_name = form.get('mother_name').strip()
        child_name = form.get('child_name').strip()
        child_dob = form.get('child_dob')
        dedication_date_time = form.get('dedication_date_time')
        officiating_minister = form.get('officiating_minister').strip()
        assembly = form.get('assembly')
        place_of_ceremony = form.get('place_of_ceremony').strip()

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
            "father_name": father_name,
            "mother_name": mother_name,
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
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    assembly_names, _, _ = utils.load_assembly_data()
                    assembly_names.insert(0, 'All')

                    cr_data = None
                    if permission == 'super_admin':
                        cr_data = RalliesAndConventions.query.all()
                    else:
                        cr_data = RalliesAndConventions.query.filter(RalliesAndConventions.assembly.ilike(f'%{current_user.assembly}%')).all()

                    return render_template('rallies-and-conventions.html', cr_data=cr_data, assembly_names=assembly_names, 
                    logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
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
        assembly = ','.join(form.getlist('assembly'))
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
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)
                    
                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    data_1 = db.session.query(Baptism, User).join(User).all()
                    bc_data = []
                    for baptism, user in data_1:
                        if permission == 'super_admin' or user.assembly == current_user.assembly:
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
                    # print(bc_data[0])
                    return render_template('baptism-certificates.html', bc_data=bc_data, logged_in_admin_data=logged_in_admin_data, 
                    logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return render_template('login.html')
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
            # if utils.member_id_exists(member_id, table="baptism"):
            #     return Response(json.dumps({'status':'FAIL', 'message': 'Member ID already exists!'}), status=400, mimetype='application/json')
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

            user_data = User.query.filter_by(member_id=member_id).first()
            fullname = user_data.last_name + ', ' + user_data.first_name + ' ' + user_data.other_names
            baptism_data = {
                "record_id":record_id,
                "member_id":member_id,
                "full_name": fullname,
                "date_of_baptism":date_of_baptism,
                "place_of_baptism":place_of_baptism,
                "officiating_minister":officiating_minister,
                "district":district,
                "area":area,
                "country":country
            }

            # return the success response to Ajax
            # return json.dumps({'status':'OK', 'message': 'successful'})
            return Response(json.dumps({'status':'OK', 'message': 'successful', 'baptism_data': baptism_data}), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            # print(form)
            return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')
        

@app.route('/load_user_by_id/<src_id_route>', methods=['POST'])
def load_user_by_id(src_id_route):
    try:
        if request.method == 'POST':
            src_id_route = src_id_route.split('member_id')
            member_id = request.form.get(f'{src_id_route[0]}member_id').strip()           
            member_data = utils.read_user_by_member_id(member_id)
            if member_data.get('assembly'):
                route = src_id_route[-1].strip().lower()
                if route == 'check' and not current_user.permission == 'super_admin' and not current_user.assembly == member_data['assembly']:
                    member_data = dict()
            return Response(json.dumps(member_data), status=200, mimetype='application/json')
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
    try:
        if current_user.is_authenticated:
            if str(current_user).split(':')[0].lower() == 'accessibility':
                permission = current_user.permission
                if permission.startswith('admin') or permission == 'super_admin':
                    logged_in_admin_data = User.query.filter_by(member_id=current_user.member_id).first()
                    logged_in_admin_img = utils.get_img_path(current_user.member_id)

                    message_count = '0'
                    if permission == 'super_admin':
                        message_count = str(utils.get_notif_count())

                    user_data = {
                            "member_id": "",
                            "first_name": "",
                            "last_name": "",
                            "other_names": "",
                            "full_name": "",
                            "gender": "Male",
                            "occupation": "",
                            "contact_1": "",
                            "contact_2": "",
                            "dob": "",
                            "email": "",
                            "marital_status": "Single",
                            "assembly": "",
                            "ministry": "",
                            "group": "Group One",
                            "comm_email": "checked",
                            "comm_sms": "checked",
                            "comm_phone": "",
                            "address_line_1": "",
                            "address_line_2": "",
                            "digital_address_code": "",
                            "region": "",
                            "district": "",
                            "country": "GH",
                            "img": "/static/assets/media/users/thecopkadna-users.png"
                        }
                    assembly_names, ministry_names, group_names = utils.load_assembly_data()
                    return render_template('add-user.html', user_data=user_data, assembly_names=assembly_names, ministry_names=ministry_names, 
                    group_names=group_names, logged_in_admin_data=logged_in_admin_data, logged_in_admin_img=logged_in_admin_img, message_count=message_count)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')

@app.route('/add_user_submit', methods=['POST'])
def add_user_submit():
    try:
        if request.method == 'POST':
            # get the form data transmitted by Ajax
            # form is an ImmutableMultiDict object
            # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.html
            form = request.form
            member_id = form.get('member_id').strip()
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

            comm_email = form.get('comm_email')
            comm_sms = form.get('comm_sms')
            comm_phone = form.get('comm_phone')
            
            address_line_1 = form.get('address_line_1').strip()
            address_line_2 = form.get('address_line_2').strip()
            digital_address_code = form.get('digital_address_code').strip()
            region = form.get('region').strip()
            district = form.get('district').strip()
            country = form.get('country')

            password = utils.generate_password()

            if member_id == "": 
                member_id = utils.gen_id(first_name, other_names, last_name)
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
                            district=district, country=country, gender=gender
                        )
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
            else:
                utils.upload_profile_photo(member_id)
                row_dict = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "other_names": other_names,
                    "occupation": occupation,
                    "email": email,
                    "marital_status": marital_status,
                    "assembly" : assembly,
                    "address_line_1": address_line_1,
                    "address_line_2": address_line_2,
                    "digital_address_code": digital_address_code,
                    "region": region,
                    "district": district,
                    "country": country,
                    "gender": gender,
                    "contact_phone_1": re.sub(r"[\+\-\s]+", "", contact_phone_1),
                    "contact_phone_2": re.sub(r"[\+\-\s]+", "", contact_phone_2),
                    "dob": dob,
                    "ministry": ",".join(ministry),
                    "group": group,
                    "comm_email": (1 if comm_email and comm_email.lower() == 'on' else 0),
                    "comm_sms": (1 if comm_sms and comm_sms.lower() == 'on' else 0),
                    "comm_phone": (1 if comm_phone and comm_phone.lower() == 'on' else 0)
                }
                User.query.filter_by(member_id=member_id).update(row_dict)
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
            return Response(json.dumps({'status':'OK', 'message': 'successful', 'member_data': utils.read_user_by_member_id(member_id)}), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        # print(form)
        return Response(json.dumps({'status':'FAIL', 'message': 'Fatal error'}), status=400, mimetype='application/json')


@app.route("/add_user_save_continue", methods=['POST'])
def add_user_save_continue():
    try:
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
                "contact_1": contact_phone_1,
                "contact_2": contact_phone_2,
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
    try:
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
                "contact_1": contact_phone_1,
                "contact_2": contact_phone_2,
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
    try:
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
                "contact_1": contact_phone_1,
                "contact_2": contact_phone_2,
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