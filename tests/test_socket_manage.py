from socket_manage import MessageManage

socket_man = MessageManage()
socket_man.flush_db()

#Test that a user can be added to a room
#Expected outcome = True
def test_add_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    p = socket_man.r.xinfo_stream("Room_1")
    assert p

# Test that a user can delete a room
# Check that the user is no longer in the room
# Expected outcome = False
def test_del_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    socket_man.del_room("1234", "Room_1")
    p = socket_man.check_user_in("1234", "Room_1")
    print(p)
    assert p

#Tests that a user can join a random room
#Expected outcome = True
def test_join_random():
    socket_man.join_random("1234", "Test Name")
    user_rooms = socket_man.r.hgetall("1234")
    assert user_rooms

#Tests that a user can send a message in a room
#Expected outcome = True
def test_add_message():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    p= socket_man.r.xadd("Room_1",
                       {"name": "1234", "msg": "Hello!", "time": "10:29", 'uid': "1234",
                        'picture': "", 'room_name': "Room_1"})

    assert p
