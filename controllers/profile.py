from flask import *
from extensions import *

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/profile', methods = ['GET'])
def profile_route():
