from flask import *
from extensions import *

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/make_comment', methods=['POST'])
def comment_route():
    if 'id' not in session: abort(404)
    cur = db.cursor()
    cur.execute("INSERT into tbl_comments (text, user_id, post_id) VALUES ('"+request.form['comment']+"', '"+str(session['id'])+"', '"+request.form['id']+"')")
    cur.execute("SELECT * FROM tbl_posts where post_id = '" + request.form['id']+"'")
    currentProfile = cur.fetchone()
    print("============================")
    print(currentProfile)
    print("============================")
    cur.close()
    return redirect("/profile?id="+str(currentProfile['user_id'])) 

@profile.route('/profile', methods = ['GET'])
def profile_route():
    options = {}
    cur = db.cursor()
    cur.execute("SELECT * from tbl_users WHERE user_id='"+request.args['id']+"'")
    user = cur.fetchone()
    cur.execute("CALL get_posts("+request.args['id']+")")
    posts = cur.fetchall()
    comments = {}
    for post in posts:
        cur.execute("CALL get_comments("+str(post['post_id'])+")")
        comments[post['post_id']] = cur.fetchall()
    cur.close()
    print("============================")
    print(comments)
    print("============================")

    if user is None: abort(404)
    options['posts'] = posts 
    options['comments'] = comments
    options['username'] = user['user_name']
    options['fname'] = user['first_name'].lower().capitalize()
    options['lname'] = user['last_name'].lower().capitalize()
    return render_template('profile.html', **options)
