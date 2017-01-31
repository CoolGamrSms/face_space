# WSGI setup
def wsgi_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    response_body = 'Hello World'
    yield response_body.encode()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('0.0.0.0', 5555, wsgi_app)
    httpd.serve_forever()

# Beginning of Flask Application
from flask import Flask, render_template, url_for, json, request
from flask.ext.mysql import MySQL
import os

# Flask App
app = Flask(__name__)

# mySQL Connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'facespace588'
app.config['MYSQL_DATABASE_DB'] = 'facespacedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Cache Busting for 'static' files
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Application Routing
@app.route('/')
@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/join/')
def join():
    return render_template('join.html')

# Sign Up Button Handler
@app.route('/join/',methods=['POST'])
def signUp():
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
            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            _hashed_password = _password
            cursor.callproc('sp_createUser',(_uname,_fname,_lname,_email,_state,_hashed_password))
            data = cursor.fetchall()
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
