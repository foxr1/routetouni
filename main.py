import os
import uuid
import datetime
import flask
import redis
from flask import Flask, render_template, session, redirect, url_for, request, send_from_directory, Blueprint
from flask_socketio import emit, join_room, leave_room, SocketIO
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from forms import LoginForm
from flask_login import login_required, current_user

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
r = redis.StrictRedis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)

main = Blueprint('main', __name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://route2uni-default-rtdb.firebaseio.com/'
})


@app.route('/sessionLogin', methods=['GET', 'POST'])
def session_login():
    id_token = request.args.get('idToken')
    # Set session expiration to 5 days.
    expires_in = datetime.timedelta(days=14)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response = flask.jsonify({'status': 'success'})
        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in
        response.set_cookie(
            'session', session_cookie, expires=expires, httponly=True, secure=True)
        return response
    except exceptions.FirebaseError:
        return flask.abort(401, 'Failed to create a session cookie')


@app.route('/sessionLogout', methods=['GET','POST'])
def session_logout():
    print("Logging out")
    session_cookie = flask.request.cookies.get('session')
    try:
        decoded_claims = auth.verify_session_cookie(session_cookie)
        auth.revoke_refresh_tokens(decoded_claims['sub'])
        response = flask.make_response(flask.redirect('/login'))
        response.set_cookie('session', expires=0)
        return response
    except auth.InvalidSessionCookieError:
        return flask.redirect('/login')


def verify_token():
    session_cookie = flask.request.cookies.get('session')
    print(session_cookie)
    if not session_cookie:
        print("No Cookie")

    else:
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            print(decoded_claims)
            return decoded_claims['uid']

        except auth.InvalidSessionCookieError:
            print("Verification Error")


@app.route('/')
def index():
    user = verify_token()
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


@app.route('/chat_index', methods=['GET', 'POST'])
@login_required
def chat_index():
    uid = uuid.uuid4()
    session['uid'] = uid
    """Login form to enter a room."""
    form = LoginForm()

    if form.validate_on_submit():
        name = form.name.data
        room = form.room.data

        session['name'] = name
        session['room'] = room

        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('chat_index.html', form=form)


def get_messages(room, start, end):
    all_msg = []
    for conv_msg in r.lrange(room, start, end):
        msg = conv_msg.split('&&')
        all_msg.append({'name': msg[1], 'msg': msg[0], 'time': msg[-1]})
    return all_msg


def get_chats():
    print('c')


@app.route('/change', methods=['GET', 'POST'])
def change():
    name = session.get('name', '')
    room = session.get('room', '')
    new_room = request.form.get('room_ch')
    session['room'] = new_room
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room, 0, 20))


@app.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room, 0, 20))


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')

    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room', "id": 'chat-' + str(room)},
         room=room, prev_msg=get_messages(room, 0, 20))


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    name = session.get('name', '')

    time = ''.join(message['time'])

    if r.rpush(room, '%s&&%s&&%s' % (message['msg'], name, time)) > 50:
        r.lpop(room)

    emit('internal_msg', {'msg': message['msg'], 'id': '#chat-' + str(room), 'name': name}, room=room, name=name)


@socketio.on('exit_room', namespace='/chat')
def exit_room(message):
    room = session.get('room')
    name = session.get('name', '')
    now = datetime.datetime.now().replace(microsecond=0).time()
    leave_msg = name + ' has left the room.'

    leave_room(room)
    emit('status', {'msg': leave_msg}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
