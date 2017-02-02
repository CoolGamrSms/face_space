from flask import *
from extensions import *

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods = ['GET'])
def login_route():
    return render_template('login.html')

@login.route('/login', methods = ['POST'])
def login_api_route():
    errormsg = []
    data = request.form
    if data == None:
        return (jsonify(errors=[{'message':"You did not provide the necessary fields"}]), 422)
    if 'username' not in data or 'password' not in data:
        errormsg.append("You did not provide the necessary fields")
        tojson = []
        for msg in errormsg:
            tojson.append({'message': msg})
        return (jsonify(errors=tojson), 422)

    username = data['username']
    password = data['password']

    if 'username' == "":
        errormsg.append("Username may not be left blank")
    if 'password' == "":
        errormsg.append("Password may not be left blank")

    if len(errormsg) != 0:
        tojson = []
        for msg in errormsg:
            tojson.append({'message': msg})
        return (jsonify(errors=tojson), 422)

    else:
        cur = db.cursor()
        cur.execute("SELECT * FROM tbl_users WHERE user_name='"+username+"'")
        user = cur.fetchone()
        if user == None:
            errormsg.append("Username does not exist")
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 404)

        elif check_password(password, user['password']):
            session['user'] = user['user_name']
            session['id'] = user['user_id']
            return redirect("/") 

        else:
            errormsg.append("Password is incorrect for the specified username")
            tojson = []
            for msg in errormsg:
                tojson.append({'message': msg})
            return (jsonify(errors=tojson), 422)

@login.route('/logout')
def logout_api_route():
    if 'id' not in session:
        tojson = []
        tojson.append({'message': 'You do not have the necessary credentials for the resource'})
        return (jsonify(errors=tojson), 401)
    session.clear()
    return redirect("/") 
