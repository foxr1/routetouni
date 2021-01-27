from socket_manage import MessageManage

socket_man = MessageManage()


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

