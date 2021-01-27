from socket_manage import MessageManage

socket_man = MessageManage()
socket_man.flush_db()


def test_add_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    p = socket_man.r.xinfo_stream("Room_1")
    assert p


def test_del_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    socket_man.del_room("1234", "Room_1")
    p = socket_man.check_user_in("1234", "Room_1")
    print(p)
    assert p


def test_join_random():
    socket_man.join_random("1234", "Test Name")
    user_rooms = socket_man.r.hgetall("1234")
    assert user_rooms


def test_add_message():
    assert False


def test_create_room():
    socket_man.create_room("user_id", "user_name", ["user_1", "user_2", "user_3", "user_4"], "Room_name")
    test = socket_man.r.xinfo_stream("user_id_0")
    assert test
