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
from flask import Flask
from flask import render_template
from flask import url_for
import os
app = Flask(__name__)

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
