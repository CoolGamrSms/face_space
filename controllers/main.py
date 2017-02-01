from flask import *
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods = ['GET'])
def main_route():
    if 'id' not in session: return render_template('login.html')
    return "you are logged in as "+session['user']
