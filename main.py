import os
from datetime import date
import flask
from flask import Flask, render_template, session, redirect, url_for, send_from_directory, Blueprint
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
    print(response)


@app.route('/')
def index():
    session_cookie = flask.request.cookies.get('session')
    if session_cookie:
        user = test_user.verify_user()
    else:
        user = None
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


@app.route('/chat')
def chat():
    test_user.verify_user()

    if not test_user.verify_user():
        return redirect(url_for('.index'))
    else:
        name = test_user.uid
        room = 'room5'
    return render_template('chat.html', name=name, room=room, prev_msg=socket_man.conv_dict(name))


@app.route('/map')
def map():
    return render_template("campus_map.html")


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    room = 'room5'
    name = test_user.uid

    join_room(room)
    emit('status', {'msg': test_user.uid + ' has entered the room', "id": str(room)},
         room=room, prev_msg=socket_man.conv_dict(name))


@socketio.on('text', namespace='/chat')
def text(message):
    room = 'room5'
    name = test_user.uid

    socket_man.add_message(room, message, name)

    emit('internal_msg', {'msg': message['msg'], 'id': str(room), 'name': name}, room=room, name=name)


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
