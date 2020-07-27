from flask import render_template, request, make_response, jsonify, Response
import json
from app import app

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
        form = request.form
        # return json.dumps({'status':'OK', 'message': 'successful'})
        return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status':'OK', 'message': 'successful'}), status=400, mimetype='application/json')


    
    


