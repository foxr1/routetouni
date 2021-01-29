"""
Name: Katie Fallon & Will Macpherson

This page tests the socket_manage.py for the
chat functionality which was created by Phillip
"""

from socket_manage import MessageManage

socket_man = MessageManage()
socket_man.flush_db()


# Test that a user can be added to a room
# Expected outcome = True

def test_add_room():
    socket_man.flush_db()
    socket_man.add_room("1234", "Room_1", "Johns_Room", "User_adding")
    new_room = socket_man.r.xinfo_stream("Room_1")
    print(new_room)
    assert new_room['first-entry'][1]['room_name'] == "Johns_Room"


# Test that a user can delete a room
# Check that the user is no longer in the room
# Expected outcome = False
def test_del_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    socket_man.del_room("1234", "Room_1")
    del_room = socket_man.check_user_in("1234", "Room_1")
    assert not del_room


# Tests that a user can join a random room
# Expected outcome = True
def test_join_random():
    socket_man.join_random("1234", "Test Name")
    user_rooms = socket_man.r.hgetall("1234")
    assert "Random_0" in user_rooms


# Tests that a user can send a message in a room
# Expected outcome = True
def test_add_message():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    socket_man.r.xadd("Room_1",
                      {"name": "1234", "msg": "Hello!", "time": "10:29", 'uid': "1234",
                       'picture': "", 'room_name': "Room_1"})
    all_msg = []
    for msg in socket_man.r.xrange("Room_1", "-", "+", count=20):
        all_msg.append(msg[1])

    assert all_msg[-1]['msg'] == "Hello!"


# Tests that a user can create a new room
# Expected outcome= True
def test_create_room():
    socket_man.create_room("user_id", "user_name", ["user_1", "user_2", "user_3", "user_4"], "Room_name")
    test = socket_man.r.xinfo_stream("user_id_0")
    assert test
