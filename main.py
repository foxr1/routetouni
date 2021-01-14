import os
from datetime import date
import flask
from flask import Flask, render_template, session, redirect, url_for, send_from_directory, Blueprint, request, \
    make_response, jsonify
from flask_socketio import emit, join_room, leave_room, SocketIO
from models import User
from socket_manage import MessageManage
from news_and_revision import web_scraper, revision

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
    test_user.logout_user()
    return index()


@app.route('/')
def index():
    if test_user.name:
        user = test_user.name
        print(user)
    else:
        session_cookie = flask.request.cookies.get('session_token')
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

@app.route('/health', methods=['GET', 'POST'])
def health():
    return render_template("health.html")

@app.route('/news', methods=['GET', 'POST'])
def news_feed():
    news_data = web_scraper.main()
    revision_data = revision.main()
    return render_template("news_feed.html", news_data=news_data, revision_data=revision_data)


@app.route('/map', methods=['GET', 'POST'])
def campus_map():
    return render_template("campus_map.html")


@app.route('/accommodation', methods=['GET', 'POST'])
def accommodation():
    return render_template("accommodation.html")


@app.route('/pubs', methods=['GET', 'POST'])
def pubs():
    return render_template("pubs_and_clubs.html")


@app.route("/chat/get_users", methods=['GET', 'POST'])
def create_entry():
    if request.method == 'GET':
        message = {'1dE06UcNkjTxMK6wlPIyd5y3h4E3': {'firstname': 'philip', 'lastname': 'solo',
                                                    'email': 'philipsolo4@gmail.com'},
                   '3AixDYlmwbSJ0b1XpyCCoqmAhL52': {'firstname': 'John', 'lastname': 'appleseed',
                                                    'email': 'johnappleseed@gmail.com'}}
        return jsonify(message)  # serialize and use JSON headers    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Success', 200


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():

    user_id = session["user_uid"]
    user_name = session["user_name"]
    user_add = []
    room_name = None

    if request.method == 'POST':
        for user in request.form:
            if user == 'chat_name':
                room_name = request.form[user]
            else:
                user_add.append(user)
        socket_man.create_room(user_id, user_name, user_add, room_name)
    return chat()


@app.route('/chat')
def chat():
    user = test_user.verify_user()

    if not user:
        return render_template("index.html", user=user)
    else:
        if test_user.name:
            session['user_uid'] = test_user.uid
            session['user_name'] = user
            session['user_image'] = test_user.picture

    return render_template('chat.html', prev_msg=socket_man.conv_dict(test_user.uid))


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    user_uid = session["user_uid"]
    user_name = session["user_name"]
    user_image = session["user_image"]
    if user_name:
        user_conv = socket_man.conv_dict(user_uid)
    else:
        return chat()

    for category in user_conv:
        for room in user_conv[category]:
            join_room(room)

            emit('status', {'name': user_name, 'uid': test_user.uid, "id": str(room), 'user_image': user_image},
                 room=room, prev_msg=user_conv)


@socketio.on('text', namespace='/chat')
def text(message):
    room = message['id']
    user_id = session["user_uid"]
    user_name = session["user_name"]
    user_image = session["user_image"]

    message['user_image'] = user_image

    if socket_man.check_user_in(user_id, room):
        socket_man.add_message(room, message, user_id)
        emit('internal_msg',
             {'msg': message['msg'], 'id': str(room), 'uid': user_id, 'name': user_name, 'user_image': user_image},
             room=room, )
    else:
        print("Error User not in room")


@socketio.on('join_random', namespace='/chat')
def join_random(message):
    user_id = session["user_uid"]
    user_name = session["user_name"]
    socket_man.join_random(user_id, user_name)


@socketio.on('exit_room', namespace='/chat')
def exit_room(message):
    user_id = session["user_uid"]

    socket_man.del_room(user_id, message['id'])

    print("exiting chat")
    leave_room(message['id'])

    emit('status', {'msg': "Has Left the room", 'name': test_user.name}, room=message['id'])


if __name__ == '__main__':
    socketio.run(app,
                 debug=True)
