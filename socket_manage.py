import datetime
from datetime import date
import redis
import os


def incr_room(room_name):
    room_listed = room_name.split('_')
    room_num = str(int(room_listed[-1]) + 1)
    return room_listed[0] + '_' + room_num


class MessageManage:

    def __init__(self):
        self.redis_host = os.environ.get('REDISHOST', 'localhost')
        self.redis_port = int(os.environ.get('REDISPORT', 6379))
        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8", decode_responses=True)

    # Add room messages from users rooms into dict
    def conv_dict(self, user_id):
        all_dict = {'random_chat': {}, 'rooms': {}}
        for room in self.get_rooms(user_id):
            msg_list = self.get_messages(room)
            if msg_list:
                if 'Random' in room:
                    all_dict['random_chat'][room] = msg_list
                    print(all_dict)
                else:
                    all_dict['rooms'][room] = msg_list
        print(all_dict)
        return all_dict

    # Get all messages from a room
    def get_messages(self, room):
        all_msg = []
        for msg in self.r.xrange(room, "-", "+", count=20):
            all_msg.append(msg[1])

        return all_msg

    # Create a new room or join existing
    def add_room(self, user_id, room_id, user_name=None, room_name=None):

        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if self.r.xgroup_create(room_id, user_id, id="$", mkstream=True):
                if user_name and self.r.xinfo_stream(room_id)['groups'] == 1:
                    self.add_message(room_id,
                                     {"name": 'server', "msg": "Chat Started by " + user_name, "time": today,
                                      "room_name": room_name},
                                     user_id, room_name)

        except redis.exceptions.ResponseError as e:
            print("User probably in group", e)
        self.r.hset(user_id, mapping={room_id: today})

    def get_rooms(self, user_id):
        user_rooms = self.r.hgetall(user_id)
        return user_rooms

    # TODO reduce z-item by one when user deletes
    def del_room(self, user_id, room_id):

        self.r.hdel(user_id, room_id)
        self.r.xgroup_destroy(room_id, user_id)

        # Delete room If empty
        if self.r.xinfo_stream(room_id)['groups'] == 1:
            print(self.r.delete(room_id))
            self.r.zpopmin("random_rooms", 1)

    def add_message(self, room_id, message, user_id, room_name=None):
        if 'user_image' not in message:
            message['user_image'] = None
        return self.r.xadd(room_id,
                           {"name": message["name"], "msg": message['msg'], "time": message['time'], 'uid': user_id,
                            'user_image': str(message['user_image']), 'room_name': str(room_name)},
                           id='*',
                           maxlen=1000,
                           approximate=True)

    def check_user_in(self, user_id, room_id):
        return self.r.hexists(user_id, room_id)

    def join_random(self, user_id, user_name):
        random_rooms = self.r.zrangebyscore("random_rooms", 0, 10)

        # If no random rooms exist or all rooms full (max 10 people)
        if not random_rooms:
            last_room = self.r.zrangebylex("random_rooms", min='-', max='+')

            # If first added room
            if not last_room:
                final_room = "Random_0"
            else:
                last_list = last_room[-1].split('_')
                room_num = str(int(last_list[-1]) + 1)
                final_room = last_list[0] + '_' + room_num

            self.r.zadd("random_rooms", mapping={final_room: 1})
            return self.add_room(user_id, final_room, user_name)
        # Join first available room
        else:
            return self.add_room(user_id, random_rooms[0])

    def create_room(self, user_id, user_name, users, room_name):

        user_rooms = list(self.get_rooms(user_id))
        user_rooms.sort()
        # Create list for personal rooms
        personal_rooms = [room for room in user_rooms if user_id in room]
        if personal_rooms:
            # Increment to avoid naming collisions
            new_room = incr_room(personal_rooms[-1])
        else:
            new_room = user_id + '_0'

        self.add_room(user_id, new_room, user_name, room_name)
        for user in users:
            self.add_room(user, new_room)

    def flush_db(self):
        self.r.flushdb()
