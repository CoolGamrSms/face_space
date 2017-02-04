from flask import *
from extensions import *

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/make_post', methods=['POST'])
def post_route():
    if 'id' not in session: abort(404)
    cur = db.cursor()
    myquery = "INSERT into tbl_posts (text, user_id) VALUES ('"+request.form['post']+"', '"+str(session['id'])+"')"
    print '======================================'
    print myquery
    print '======================================'
    cur.execute(myquery)
    cur.close()
    return redirect("/home")

@home.route('/make_comment_from_home', methods=['POST'])
def comment_route():
    if 'id' not in session: abort(404)
    cur = db.cursor()
    cur.execute("INSERT into tbl_comments (text, user_id, post_id) VALUES ('"+request.form['comment']+"', '"+str(session['id'])+"', '"+request.form['id']+"')")
    cur.close()
    return redirect("/home/#post-"+request.form['id'])

@home.route('/home/', methods = ['GET'])
def home_route():
    if 'id' not in session: return redirect('/')
    options = {}
    cur = db.cursor()
    cur.execute("SELECT * from tbl_users WHERE user_id='"+str(session['id'])+"'")
    user = cur.fetchone()
    cur.execute("CALL get_friendsPosts("+str(user['user_id'])+")")
    feedPosts = cur.fetchall()
    cur.execute("CALL get_friends("+str(user['user_id'])+")")
    friends = cur.fetchall()
    comments = {}
    for post in feedPosts:
        post['first_name'] = post['first_name'].lower().capitalize()
        post['last_name'] = post['last_name'].lower().capitalize()
        cur.execute("CALL get_comments("+str(post['post_id'])+")")
        comments[post['post_id']] = cur.fetchall()
        for comment in comments[post['post_id']]:
            comment['first_name'] = comment['first_name'].lower().capitalize()
            comment['last_name'] = comment['last_name'].lower().capitalize()

    cur.execute("CALL get_pending("+str(session['id'])+")")
    options['pending'] = cur.rowcount
    cur.close()

    for friend in friends:
        friend['full_name'] = friend['first_name'].lower().capitalize() + " " + friend['last_name'].lower().capitalize()


    options['feedPosts'] = feedPosts
    options['comments'] = comments
    options['friends'] = friends
    options['username'] = user['user_name']
    options['user_id'] = user['user_id']
    options['fname'] = user['first_name'].lower().capitalize()
    options['lname'] = user['last_name'].lower().capitalize()
    return render_template('home.html', **options)
