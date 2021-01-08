from datetime import date
import redis
import os


class MessageManage:

    def __init__(self):

        self.redis_host = os.environ.get('REDISHOST', 'localhost')
        self.redis_port = int(os.environ.get('REDISPORT', 6379))
        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8", decode_responses=True)

    def conv_dict(self, user_id):
        # r.hset(test_user.uid, mapping={"room5": "14/11/2000", "Room-15": "15/11/2000"})
        # r.rpush("room5", '%s&&%s&&%s' % ("What it is",test_user.uid, "12:30"))

        all_dict = {}
        for room in self.get_rooms(user_id):
            msg_list = self.get_messages(room, 0, 20)
            all_dict[room] = msg_list
        return all_dict

    def get_messages(self, room, start, end):
        all_msg = []
        for conv_msg in self.r.lrange(room, start, end):
            msg = conv_msg.split('&&')
            all_msg.append({'name': msg[1], 'msg': msg[0], 'time': msg[-1]})
        return all_msg

    def add_room(self, user_id, room_id):

        today = date.today().strftime("%d/%m/%Y")

        self.r.hset(user_id, mapping={room_id: today})
        self.r.hset(room_id, mapping={user_id: today})

    def get_rooms(self, user_id):
        user_rooms = self.r.hgetall(user_id)
        return user_rooms

    def del_room(self, user_id, room_id):
        response = self.r.hdel(user_id, room_id)
        return response

    def add_message(self, room_id, message, user_name):

        time = ''.join(message['time'])
        if self.r.rpush(room_id, '%s&&%s&&%s' % (message['msg'], user_name, time)) > 50:
            self.r.lpop(room_id)
