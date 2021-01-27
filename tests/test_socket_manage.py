from socket_manage import MessageManage

socket_man = MessageManage()


def test_add_room():
    socket_man.add_room("1234", "Room_1", "room_name", "User_adding")
    p = socket_man.r.xinfo_stream("Room_1")
    assert p


def test_create_room():
    socket_man.create_room("1234", "Room_1", ["user_1", "user_2", "user_3", "user_4"], "User_Creating")
    t = socket_man.r.xinfo_stream("1234")
    assert t

    # create_room, check_user_in
