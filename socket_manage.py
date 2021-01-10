from datetime import date
import redis
import os


class MessageManage:

    def __init__(self):

        self.redis_host = os.environ.get('REDISHOST', 'localhost')
        self.redis_port = int(os.environ.get('REDISPORT', 6379))
        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8", decode_responses=True)

    def conv_dict(self, user_id):
        all_dict = {}
        for room in self.get_rooms(user_id):
            msg_list = self.get_messages(room)
            if msg_list:
                all_dict[room] = msg_list
        return all_dict

    def get_messages(self, room):
        all_msg = []
        for msg in self.r.xrange(room, "-", "+", count=20):
            all_msg.append(msg[1])

        return all_msg

    def add_room(self, user_id, room_id):
        today = date.today().strftime("%d/%m/%Y")
        try:
            self.r.xgroup_create(room_id, user_id, id="$", mkstream=True)

        except redis.exceptions.ResponseError as e:
            print("Error Creating group prob already exists", e)

        self.r.hset(user_id, mapping={room_id: today})

    def get_rooms(self, user_id):
        user_rooms = self.r.hgetall(user_id)
        return user_rooms

    def del_room(self, user_id, room_id):
        self.r.hdel(user_id, room_id)
        self.r.xgroup_destroy(room_id, user_id)

        # Delete room If empty
        if self.r.xinfo_stream(room_id)['groups'] == 0:
            self.r.delete(room_id)

    def add_message(self, room_id, message, user_id, user_name):

        print(self.r.xadd(room_id, {"name": user_name, "msg": message['msg'], "time": message['time'],'uid': user_id}, id='*',
                          maxlen=1000,
                          approximate=True))

    def check_user_in(self, user_id, room_id):
        return self.r.hexists(user_id, room_id)

    def join_random(self, user_id):
        random_rooms = self.r.zrangebyscore("random_rooms", 0, 10)
        if not random_rooms:
            self.r.zadd("random_rooms", mapping={"Random_1": 1})
            self.add_room(user_id, "Random_1")
        else:
            self.add_room(user_id, random_rooms[0])
