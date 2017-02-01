from flask import *
from extensions import *

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/profile', methods = ['GET'])
def profile_route():
    options = {}
    cur = db.cursor()
    cur.execute("SELECT * from tbl_users WHERE user_id='"+request.args['id']+"'")
    user = cur.fetchone()
    cur.close()
    if user is None: abort(404)
    options['username'] = user['user_name']
    options['fname'] = user['first_name'].lower().capitalize()
    options['lname'] = user['last_name'].lower().capitalize()
    return render_template('profile.html', **options)
