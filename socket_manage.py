import datetime
import redis
import os

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))


def incr_room(room_name: str) -> str:
    """
    :param room_name: a name to increment by 1
    :return: an incremented version of the room name
    """
    room_listed = room_name.split('_')
    room_num = str(int(room_listed[-1]) + 1)
    return room_listed[0] + '_' + room_num


class MessageManage:
    """
    A class for managing Redis and user messaging.

    :Authors:
        Filippos Solomonidis <F.solomonidis2@newcastle.ac.uk>
    ...
    Attributes
    ----------
     r_host: str
        ip of the redis db to connect

     r_port: int
        port of redis db to connect


    Methods
    -------
    conv_dict(user_id):
        Returns all users conversations in the form of a dictionary

    get_messages(room):
        Returns all messages within a particular room

    get_rooms(ser_id):
        Get all rooms user is in

    add_room(user_id, room_id, room_name=None, user_name=None):
        Creates a room in the Redis database with the specified credentials, adds user to room if already exists

    create_room(user_id, user_name, users, room_name):
        In order to avoid naming collisions, if the user creates a room, his username with a corresponding number is
        added (starting _0 increased each time new room is created)

    del_room(user_id, room_id):
        Remove a room form the database, if the user created the room it is deleted, or in the case of
        a random room, if it is empty it is deleted

    check_user_in(user_id, room_id):
        check database  if user in the specific room

    join_random(user_id, user_name):
        Join first available random chat, if no chats exist, one is created, each time one contains 10 people,
        a new chat is created

    flush_db():
        clear the Redis database
    """

    def __init__(self, r_host: str = redis_host, r_port: int = redis_port):
        self.r = redis.StrictRedis(host=r_host, port=r_port, charset="utf-8", decode_responses=True)

    # Add room messages from users rooms into dict
    def conv_dict(self, user_id: str) -> dict:
        """
        :param user_id: the users id
        :return: all_dict a dictinary containing all user conversations
        """
        all_dict = {'random_chat': {}, 'rooms': {}}
        for room_id, room_name in self.get_rooms(user_id).items():
            msg_list = self.get_messages(room_id)
            if msg_list:
                if 'Random' in room_id:
                    all_dict['random_chat'][room_id] = {'msgs': msg_list, 'room_name': room_name}
                else:
                    all_dict['rooms'][room_id] = {'msgs': msg_list, 'room_name': room_name}
        return all_dict

    # Get all messages from a room
    def get_messages(self, room: str) -> list:
        """
        :param room: A room to retrieve conversations from
        :return: A list with all the conversations in ascending order sent
        """
        all_msg = []
        for msg in self.r.xrange(room, "-", "+", count=20):
            all_msg.append(msg[1])
        return all_msg

    def get_rooms(self, user_id: str) -> dict:
        """
        :param user_id:
        :return: dictionary of all rooms user is in
        """
        user_rooms = self.r.hgetall(user_id)
        return user_rooms

    def create_room(self, user_id: str, user_name: str, users: list, room_name: str) -> None:
        """
        :param user_id: the users id
        :param user_name: users name
        :param users: a list with the users to be added to the created room
        :param room_name: name for the new room
        """
        user_rooms = list(self.get_rooms(user_id))
        user_rooms.sort()
        # Create list for personal rooms
        personal_rooms = [room for room in user_rooms if user_id in room]
        if personal_rooms:
            # Increment to avoid naming collisions
            new_room = incr_room(personal_rooms[-1])
        else:
            new_room = user_id + '_0'

        self.add_room(user_id, new_room, room_name, user_name)
        for user in users:
            self.add_room(user, new_room, room_name)

    # Create a new room or join existing
    def add_room(self, user_id: str, room_id: str, room_name=None, user_name=None) -> None:
        """
        :param user_id: the users id
        :param room_id: the id of the room to add the user
        :param room_name: name in the case it is the first time room is created
        :param user_name: default user name to add for the server creation message
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if self.r.xgroup_create(room_id, user_id, id="$", mkstream=True):
                if user_name and self.r.xinfo_stream(room_id)['groups'] == 1:
                    self.add_message(room_id,
                                     {"name": 'server', "msg": "Chat Started by " + user_name, "time": today,
                                      "room_name": room_name, "picture": "../static/images/chat/server_image.png"},
                                     user_id, room_name)
        except redis.exceptions.ResponseError as e:
            print("User probably in group", e)
        self.r.hset(user_id, mapping={room_id: room_name})

    def del_room(self, user_id: str, room_id: str) -> None:
        """
        :param user_id: the users id
        :param room_id: the id of the room to delete the user from
        """
        # Remove user from personal rooms list
        self.r.hdel(user_id, room_id)
        # Remove user from room store
        self.r.xgroup_destroy(room_id, user_id)

        # Decrease number of people if random chat
        if "Random" in room_id:
            self.r.zincrby("random_rooms", -1, room_id)

        # Delete room If last exiting
        if self.r.xinfo_stream(room_id)['groups'] == 0:
            self.r.delete(room_id)
            self.r.delete("random_rooms", room_id)
        # Delete Room if created by user
        elif user_id in room_id:
            self.r.delete(room_id)

    def add_message(self, room_id: str, message: dict, user_id: str, room_name=None) -> str:
        """
        :param room_id: id of room to add the message
        :param message: dictionary containing all message information (time, room_id, picture)
        :param user_id: id of the user that sent the message
        :param room_name: name of room
        :return: id of where the message was added in the db
        """
        if 'picture' not in message:
            message['picture'] = None
        return self.r.xadd(room_id,
                           {"name": message["name"], "msg": message['msg'], "time": message['time'], 'uid': user_id,
                            'picture': str(message['picture']), 'room_name': str(room_name)},
                           id='*',
                           maxlen=1000,
                           approximate=True)

    def check_user_in(self, user_id: str, room_id: str) -> bool:
        """
        :param user_id: user id to query
        :param room_id: room to see if withing the users room dict
        :return: Boolean if the user is in the room
        """
        return self.r.hexists(user_id, room_id)

    def join_random(self, user_id: str, user_name: str) -> None:
        """
        :param user_id: the users id
        :param user_name: the users name
        :return: None
        """
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
            return self.add_room(user_id, final_room, final_room, user_name)

        # Join first available room
        else:
            self.r.zincrby("random_rooms", 1, random_rooms[0])
            return self.add_room(user_id, random_rooms[0], random_rooms[0])

    def flush_db(self):
        self.r.flushdb()
