from flask import *
from extensions import db, hash_password

join = Blueprint('join', __name__, template_folder='templates')

@join.route('/join/')
def join_route():
    return render_template("join.html")

@join.route('/join/',methods=['POST'])
def sign_up_route():
    cur = db.cursor()
    try:
        # read the posted values from the UI
        _uname = request.form['new_uname']
        _fname = request.form['new_fname']
        _lname = request.form['new_lname']
        _email = request.form['new_email']
        _state = request.form['new_state']
        _password = request.form['new_password']
        if _uname and _fname and _lname and _email and _state and _password:
            # Call MySQL
            #_hashed_password = generate_password_hash(_password)
            _hashed_password = hash_password(_password)
            print(_hashed_password)
            cmd = "INSERT into tbl_users (first_name, last_name, user_name, email, state, password) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(cmd, [_fname, _lname, _uname, _email, _state, _hashed_password])
            data = cur.fetchall()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

        if len(data) is 0:
            return redirect('/')
        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    cur.close()
