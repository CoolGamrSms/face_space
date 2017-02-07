from flask import *
from extensions import db, hash_password

password = Blueprint('password', __name__, template_folder='templates')

@password.route('/password')
def password_route():
    if 'id' not in session: abort(404)
    options = {}
    if 'error' in request.args:
        options['error'] = request.args['error']
        return render_template("password.html", **options)
    else:
        return render_template("password.html")

@password.route('/password',methods=['POST'])
def password_change_route():
    if 'id' not in session: abort(404)
    cur = db.cursor()
    try:
        # read the posted values from the UI
        _password = request.form['new_password']
        _confirmPassword = request.form['confirm_new_password']

        if _password != _confirmPassword:
            return redirect('password?error=1')

        if _password and _confirmPassword:
            # Call MySQL
            #_hashed_password = generate_password_hash(_password)
            _hashed_password = hash_password(_password)
            print(_hashed_password)
            cur.execute("UPDATE tbl_users SET password = '"+_hashed_password+"' WHERE user_id = '"+str(session['id'])+"'")
            print "==========================="
            print "PASSWORD CHANGED FOR USER "+str(session['id']) 
            print "==========================="
            return redirect('/home')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

        """
        if len(data) is 0:
            return redirect('/')
        else:
            return json.dumps({'error':str(data[0])})
        """

    except Exception as e:
        return json.dumps({'error':str(e)})
    cur.close()
