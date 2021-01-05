import os
import redis
from flask import Flask, render_template, session, redirect, url_for, request, send_from_directory, Blueprint
from flask_socketio import emit, join_room, leave_room, SocketIO
from models import User


redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
r = redis.StrictRedis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)

main = Blueprint('main', __name__)

test_user = User()


@app.route('/sessionLogin', methods=['GET', 'POST'])
def session_login():
    print('logging in ')
    response = test_user.login_user()
    return response


@app.route('/sessionLogout', methods=['GET', 'POST'])
def session_logout():
    response = test_user.logout_user()
    print(response)


@app.route('/')
def index():
    user = test_user.verify_user()
    if test_user.email:
        print(test_user.email, test_user.uid)
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


def get_messages(room, start, end):
    all_msg = []
    for conv_msg in r.lrange(room, start, end):
        msg = conv_msg.split('&&')
        all_msg.append({'name': msg[1], 'msg': msg[0], 'time': msg[-1]})
    return all_msg


@app.route('/change', methods=['GET', 'POST'])
def change():
    name = session.get('name', '')
    room = session.get('room', '')
    new_room = request.form.get('room_ch')
    session['room'] = new_room
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room, 0, 20))


@app.route('/chat')
def chat():
    name = test_user.uid
    room = 5

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room, 0, 20))


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    room = 5

    join_room(room)
    emit('status', {'msg': test_user.uid + ' has entered the room', "id": 'chat-' + str(room)},
         room=room, prev_msg=get_messages(room, 0, 20))


@socketio.on('text', namespace='/chat')
def text(message):
    room = 5
    name = test_user.uid

    time = ''.join(message['time'])

    if r.rpush(room, '%s&&%s&&%s' % (message['msg'], name, time)) > 50:
        r.lpop(room)

    emit('internal_msg', {'msg': message['msg'], 'id': '#chat-' + str(room), 'name': name}, room=room, name=name)


@socketio.on('exit_room', namespace='/chat')
def exit_room(message):
    room = 5
    name = test_user.uid

    leave_msg = name + ' has left the room.'

    leave_room(room)
    emit('status', {'msg': leave_msg}, room=room)


if __name__ == '__main__':
    socketio.run(app, port=5000,
                 cors_allowed_origins=["https://extreme-lattice-298010.nw.r.appspot.com:5000", "http://extreme-lattice"
                                                                                          "-298010.nw.r.appspot.com:5000"],
                 debug=True)
