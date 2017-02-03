from flask import *
from extensions import *

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route('/make_comment', methods=['POST'])
def comment_route():
    if 'id' not in session: return redirect('/')
    cur = db.cursor()
    cur.execute("INSERT into tbl_comments (text, user_id, post_id) VALUES ('"+request.form['comment']+"', '"+str(session['id'])+"', '"+request.form['id']+"')")
    cur.execute("SELECT * FROM tbl_posts where post_id = '" + request.form['id']+"'")
    currentProfile = cur.fetchone()
    cur.close()
    return redirect("/profile/"+str(currentProfile['user_id'])+"#post-"+request.form['id'])

@profile.route('/profile/<id>', methods = ['GET'])
def profile_route(id):
    if 'id' not in session: return redirect('/')
    options = {}
    cur = db.cursor()
    cur.execute("SELECT * from tbl_users WHERE user_id='"+id+"'")
    user = cur.fetchone()


    if user is None: abort(404)
    cur.execute("CALL get_posts("+id+")")

    id = long(id)

    posts = cur.fetchall()
    comments = {}
    for post in posts:
        cur.execute("CALL get_comments("+str(post['post_id'])+")")
        comments[post['post_id']] = cur.fetchall()
        for comment in comments[post['post_id']]:
            comment['first_name'] = comment['first_name'].lower().capitalize()
            comment['last_name'] = comment['last_name'].lower().capitalize()
    cur.execute("CALL get_friends("+str(id)+")")
    options['friends'] = cur.rowcount
    cur.execute("SELECT status, friends_since, action_user_id FROM tbl_relationships WHERE user_id='"+str(min(session['id'], id))+"' AND friend_id='"+str(max(session['id'], id))+"'")
    status = -2
    since = 0
    if cur.rowcount == 0:
        status = -1
    else:
        answer = cur.fetchone()
        if answer['action_user_id'] != session['id'] and answer['status'] == 0:
            status = 2
        else:
            status = answer['status']
        since = answer['friends_since']
    if session['id'] == id:
        status = -2
    cur.close()

    options['since'] = since
    options['status'] = status
    options['posts'] = posts
    options['comments'] = comments
    options['username'] = user['user_name']
    options['fname'] = user['first_name'].lower().capitalize()
    options['lname'] = user['last_name'].lower().capitalize()
    return render_template('profile.html', **options)
