import json
import os
import flask
from flask import Flask, render_template, session, send_from_directory, Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room, SocketIO
from models import User, get_all_users, get_mentors, get_verified
from socket_manage import MessageManage
from news_and_revision import web_scraper

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax')

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins=["https://extreme-lattice-298010.nw.r.appspot.com",
                                                                      "http://extreme-lattice-298010.nw.r.appspot.com",
                                                                      "http://localhost:5000",
                                                                      "https://routetouni.me"],
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
    test_user.logout_user()
    return index()


@app.route('/')
def index():
    if "name" not in session:
        session_cookie = flask.request.cookies.get('session_token')
        if session_cookie:
            user = test_user.verify_user
        else:
            user = None
    else:
        user = session['user_dict']
    return render_template("index.html", user=user)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    session_cookie = flask.request.cookies.get('session_token')
    if session_cookie:
        user = test_user.verify_user
        if user.get('role') == 'admin':
            return render_template("admin.html", unverified_mentors=get_mentors(),
                                   verified_mentors=get_verified())
        else:
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


@app.route('/health', methods=['GET', 'POST'])
def health():
    return render_template("health.html")


@app.route('/news', methods=['GET', 'POST'])
def news_feed():
    news_data = web_scraper.main()
    return render_template("news_feed.html", news_data=news_data)


@app.route('/revision', methods=['GET', 'POST'])
def revision_feed():
    return render_template("revision.html")


@app.route('/map', methods=['GET', 'POST'])
def campus_map():
    return render_template("campus_map.html")


@app.route('/accommodation', methods=['GET', 'POST'])
def accommodation():
    return render_template("accommodation.html")


@app.route('/pubs', methods=['GET', 'POST'])
def pubs():
    return render_template("pubs.html")


@app.route('/societies', methods=['GET', 'POST'])
def societies():
    return render_template("societies.html")


@app.route('/revision', methods=['GET', 'POST'])
def revision():
    return render_template("revision.html")


@app.route('/chat')
def chat():
    user = test_user.verify_user
    if not user:
        return render_template("index.html", user=user)
    else:

        return render_template('chat.html', prev_msg=socket_man.conv_dict(user.get('uid')), user_name=user.get('name'))


@app.route("/chat/get_users", methods=['GET', 'POST'])
def create_entry():
    if request.method == 'GET':
        ref = get_all_users()
        ref.pop(session['user_dict'].get('uid'))
        return jsonify(ref)
    if request.method == 'POST':
        return 'Success', 200


@app.route('/chat/create_chat', methods=['GET', 'POST'])
def create_chat():
    user_dict = session['user_dict']

    user_add = []
    room_name = None
    if request.method == 'POST':
        form_json = request.get_json()
        for item in form_json:
            if item.get('name') == 'chat_name':
                room_name = item['value']
            else:
                user_add.append(item['name'])

        socket_man.create_room(user_dict.get('uid'), user_dict.get('name'), user_add, room_name)
        return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    user_dict = session['user_dict']

    if user_dict.get('name'):
        user_conv = socket_man.conv_dict(user_dict.get('uid'))
    else:
        return chat()

    for category in user_conv:
        for room in user_conv[category]:
            join_room(room)

            emit('status', {'msg': "Has Joined the Chat", 'name': user_dict.get('name'), 'uid': user_dict['uid'],
                            "room_id": str(room), 'color': 'success', 'user_image': user_dict.get('picture')},
                 room=room, prev_msg=user_conv, user_name=user_dict.get('name'))


@socketio.on('text', namespace='/chat')
def text(message):
    user_dict = session['user_dict']

    # Room Message arrived from
    room = message['room_id']

    # Add the user picture to the redis store
    message['picture'] = user_dict.get('picture')

    if socket_man.check_user_in( user_dict.get('uid'), room):
        socket_man.add_message(room, message,  user_dict.get('uid'))
        emit('internal_msg',
             {'msg': message['msg'], 'room_id': str(room), 'uid':  user_dict.get('uid'), 'name': user_dict.get('name'),
              'user_image': user_dict.get('picture')},
             room=room, user_name=user_dict.get('name'))
    else:
        print("Error User not in room")


@socketio.on('join_random', namespace='/chat')
def join_random(message):
    user_dict = session['user_dict']
    socket_man.join_random(user_dict.get('uid'), user_dict.get('uid'))


@socketio.on('exit_room', namespace='/chat')
def exit_room(message):
    user_dict = session['user_dict']
    socket_man.del_room(user_dict.get('uid'), message['room_id'])
    leave_room(message['room_id'])
    emit('status', {'msg': "Has left the Chat", 'name': user_dict.get('name'), 'color': 'danger'}, room=message['room_id'],
         user_name=user_dict.get('name'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
