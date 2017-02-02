from flask import *
from extensions import *

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/home/')
def home_route():
    options = {}
    cur = db.cursor()
    cur.execute("SELECT * from tbl_users WHERE user_name='"+session['user']+"'")
    user = cur.fetchone()
    cur.execute("CALL get_friendsPosts("+str(user['user_id'])+")")
    feedPosts = cur.fetchall()
    cur.execute("CALL get_friends("+str(user['user_id'])+")")
    friends = cur.fetchall()
    comments = {}
    for post in feedPosts:
        cur.execute("CALL get_comments("+str(post['post_id'])+")")
        comments[post['post_id']] = cur.fetchall()
    cur.close()
    print("============================")
    print(str(user['user_id']))
    print("============================")

    if user is None: abort(404)
    options['feedPosts'] = feedPosts 
    options['comments'] = comments
    options['friends'] = friends
    options['username'] = user['user_name']
    options['fname'] = user['first_name'].lower().capitalize()
    options['lname'] = user['last_name'].lower().capitalize()
    return render_template('home.html')