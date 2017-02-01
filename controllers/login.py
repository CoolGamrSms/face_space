from flask import *
from extensions import *

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods = ['GET'])
def login_route():
	return render_template("login.html")
