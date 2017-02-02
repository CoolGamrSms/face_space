from flask import Flask, render_template, url_for
import extensions
import controllers
import os

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

## Replace controllers below
app.register_blueprint(controllers.join)
app.register_blueprint(controllers.profile)
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.login)
app.register_blueprint(controllers.home)

app.secret_key = '\xe59\xee\x93`\xd8\xfa\xe8\x00\x9f\xc7\x8d|\xec\xe3U\xad\xab\x88#\xe7\xa6\xda\xf9'

###########################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html'), 404

@app.errorhandler(403)
def forbidden(e):
	return render_template('forbidden.html'), 403

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)

# Cache Busting for 'static' files (Primarily CSS)
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
