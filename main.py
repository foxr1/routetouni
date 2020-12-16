import os
import uuid
import datetime
import redis
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, Response, send_from_directory
from flask_socketio import emit, join_room, leave_room, SocketIO
from news_and_revision import revision, web_scraper

# Connect to redis on Docker
# r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

# Connect to redis on GCP

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
r = redis.StrictRedis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


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
    revision_list = revision.main()
    news_list = web_scraper.main()
    return render_template("news_feed.html")


def get_messages(room):
    all_msg = []
    while r.llen(room) != 0:
        print(r.lpop(room))
        if r.lpop(room):
            msg = r.lpop(room).split(')(')
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
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room))


@app.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, prev_msg=get_messages(room))


# When Client Enters
@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(5)
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room'},
         room=room, prev_msg=get_messages(room))


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    name = session.get('name', '')

    time = ''.join(message['time'])
    r.zadd('mykey', 'b', 2)
    print(r.zcard('mykey'))
    r.rpush(room, '%s)(%s)(%s' % (message['msg'], name, time))

    emit('internal_msg', {'msg': message['msg'], 'id': '#chat', 'name': name}, room=room, name=name)


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
