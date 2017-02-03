from flask import *
from extensions import *

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search', methods = ['GET'])
def search_route():
    if 'id' not in session: return redirect('/')
    options = {}
    query = request.args['q']
    options['query'] = query
    cur = db.cursor()
    if query.count(' ') == 1:
        fname, lname = query.split(' ')
        cur.execute("SELECT * FROM tbl_users WHERE user_id != '"+str(session['id'])+"' AND first_name LIKE '%"+fname+"%' AND last_name LIKE '%"+lname+"%'")
    elif '@' in query:
        cur.execute("SELECT * FROM tbl_users WHERE user_id != '"+str(session['id'])+"' AND email='"+query+"'")
    else:
        cur.execute("SELECT * FROM tbl_users WHERE user_id != '"+str(session['id'])+"' AND first_name LIKE '%"+query+"%' OR last_name LIKE '%"+query+"%' OR user_name LIKE '%"+query+"%'")
    options['results'] = cur.fetchall()
    for friend in options['results']:
        friend['full_name'] = friend['first_name'].lower().capitalize() + " " + friend['last_name'].lower().capitalize()
        friend['user_id'] = long(friend['user_id'])
        cur.execute("SELECT status, friends_since, action_user_id FROM tbl_relationships WHERE user_id='"+str(min(session['id'], friend['user_id']))+"' AND friend_id='"+str(max(session['id'], friend['user_id']))+"'")
        if cur.rowcount == 0:
            friend['status'] = -1
        else:
            answer = cur.fetchone()
            if answer['action_user_id'] != session['id'] and answer['status'] == 0:
                friend['status'] = 2
            else:
                friend['status'] = answer['status']
            friend['ship'] = answer['friends_since']
    return render_template('search.html', **options)
