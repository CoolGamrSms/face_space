from flask import *
from extensions import *

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/home/')
def home_route():
    return render_template('home.html')