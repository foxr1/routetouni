import os
from datetime import date
import flask
from flask import Flask, render_template, session, redirect, url_for, send_from_directory, Blueprint, request
from flask_socketio import emit, join_room, leave_room, SocketIO
from models import User
from socket_manage import MessageManage

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins=["https://extreme-lattice-298010.nw.r.appspot.com",
                                                                      "http://extreme-lattice-298010.nw.r.appspot.com",
                                                                      "http://localhost:5000"],
                    logger=True, engineio_logger=True)

main = Blueprint('main', __name__)

test_user = User()
socket_man = MessageManage()


@app.route('/sessionLogin', methods=['GET', 'POST'])
def session_login():
    response = test_user.login_user()
    return response


@app.route('/sessionLogout', methods=['GET', 'POST'])
def session_logout():
    response = test_user.logout_user()
    return response


@app.route('/')
def index():
    session_cookie = flask.request.cookies.get('session')
    if test_user.name:
        user = True
    else:
        if session_cookie:
            user = test_user.verify_user()
        else:
            user = False

    return render_template("index.html", user=user)


@app.route('/gregister')
def gregister():
    return render_template("google_login.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/news_feed')
def news_feed():
    return render_template("news_feed.html")


@app.route('/map')
def camp_map():
    return render_template("campus_map.html")


@app.route('/chat')
def chat():
    if not test_user.verify_user():
        return redirect(url_for('.index'))
    else:
        user_uid = test_user.uid

        socket_man.add_message("Random_1",
                               {"name": test_user.name, "msg": "Hallo what it is", "time": '13:55:30 | Jan 9'},
                               user_uid, test_user.name)

    return render_template('chat.html', name=test_user.name, prev_msg=socket_man.conv_dict(user_uid))


@app.route('/exit_chat', methods=['GET', 'POST'])
def exit_chat():
    name = test_user.uid
    if request.method == 'POST':
        room_id = request.form['exit_butt']
        socket_man.del_room(name, room_id)
    print("exiting chat")
    return chat()


@app.route('/random_chat', methods=['GET', 'POST'])
def join_random():
    uid = test_user.uid
    if request.method == 'POST':
        socket_man.join_random(uid)
    return chat()


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    user_uid = test_user.uid
    user_name = test_user.name
    user_conv = socket_man.conv_dict(user_uid)

    for room in user_conv:
        join_room(room)

        socket_man.add_message(room,
                               {'name': test_user.name, 'msg': 'User has Joined', 'uid': test_user.uid, "id": str(room),
                                'time': message['time']}, user_uid, user_name)
        emit('status', {'name': user_name, 'uid': test_user.uid, "id": str(room)},
             room=room, prev_msg=user_conv)


@socketio.on('text', namespace='/chat')
def text(message):
    room = message['id']
    user_name = test_user.name
    user_id = test_user.uid

    if socket_man.check_user_in(user_id, room):
        socket_man.add_message(room, message, user_id, user_name)
        emit('internal_msg', {'msg': message['msg'], 'id': str(room), 'uid': user_id, 'name': user_name}, room=room,
             name=user_name)
    else:
        print("Error User not in room")


@socketio.on('exit_room', namespace='/chat')
def exit_room(message):
    room = 'room5'
    name = test_user.uid

    leave_msg = name + ' has left the room.'

    leave_room(room)
    emit('status', {'msg': leave_msg}, room=room)


if __name__ == '__main__':
    socketio.run(app,
                 debug=True)
