from flask import *
from extensions import *

friends = Blueprint('friends', __name__, template_folder='templates')

#route to view pending friend requests
@friends.route('/friends', methods = ['GET'])
def friends_route():
    if 'id' not in session: return redirect('/')


    return render_template('friends.html')
#route to accept a request
@friends.route('/friends/accept/<id>', methods = ['GET'])
def friends_accept_route(id):
    if 'id' not in session: return redirect('/')

    id = long(id)

    cur = db.cursor()
    cur.execute("UPDATE tbl_relationships SET status = 1, action_user_id = "+str(session['id'])+" WHERE user_id = "+str(min(id, session['id']))+" AND friend_id = "+str(max(id, session['id'])))
    cur.close()

    return redirect('/profile/'+str(id))

#route to decline/cancel a request or unfriend
@friends.route('/friends/delete/<id>', methods = ['GET'])
def friends_delete_route(id):
    if 'id' not in session: return redirect('/')

    id = long(id)

    cur = db.cursor()
    cur.execute("DELETE FROM tbl_relationships WHERE user_id="+str(min(id, session['id']))+" AND friend_id="+str(max(id, session['id'])));
    cur.close()
    return redirect('/profile/'+str(id))
#route to create a request
@friends.route('/friends/add/<id>', methods = ['GET'])
def friends_add_route(id):
    if 'id' not in session: return redirect('/')

    id = long(id)

    cur = db.cursor()
    cur.execute("INSERT INTO `tbl_relationships` (`user_id`, `friend_id`, `status`, `action_user_id`) VALUES ("+str(min(id, session['id']))+", "+str(max(id, session['id']))+", 0, "+str(session['id'])+")");
    cur.close()

    return redirect('/profile/'+str(id))
