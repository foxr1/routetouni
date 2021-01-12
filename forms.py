import redis
import os
from datetime import date

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
r = redis.StrictRedis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

user = {"Name": "Pradeep", "Company": "SCTL", "Address": "Mumbai", "Location": "RCP"}

# print(r.rpushx("random","random_1"))
print(r.zadd("random_rooms",mapping={"Random_0": 1}))
#
# print(r.xadd("Random1", {"name":"kk"},id='*',maxlen=500,approximate=True))

# print(r.xgroup_create("john","peter_stream",id="$"))

# print(r.xgroup_destroy("peter","peter_stream"))
# print(r.xgroup_destroy("peter","*"))

# r.xgroup_create("Random1","group2",id="$")
# r.xgroup_destroy("Random1","group2")

# print(r.xtrim("peter",6,approximate=True))

print(r.xinfo_groups("Random_0"))
print(r.xinfo_stream("Random_0"))
#     r.delete("Random1")

# if r.xlen("Random1") > 3:
# for msg in r.xrange("Random1","-","+",count=20):
#     print(r.xdel("Random1",msg[0]))


# print(r.xadd("Random_1", {"name": "philip solo", "msg": "WHAT IT IS", "time": "14:23"}, id='*', maxlen=500,
#                   approximate=True))


# print(r.xlen("john"))
# r.hset("ROOM_ID", mapping={"USERI5": "DATE_JOINED", "USERI6": "DATE_JOINED"})
# print(r.zadd("random_rooms", mapping={"Random_1": 0}))
# print(r.zadd("random_rooms", mapping={"Random_2": 3}))
# print(r.zincrby("random_rooms",3,"Random_1"))

#
# print(r.zscore("random_rooms","Random_3"))
# last = (r.zrangebylex("random_rooms",min='-',max='+')[-1])

# print(r.zpopmin("random_rooms", 1))
for elem in r.zscan_iter("random_rooms"):
    print(elem)
# print(r.zrange("random_rooms",0,5))

# print()
# print(r.hexists("Room 5", "3boNDH3ypRaBX9pc27ZYz049qNP2"))

# print(r.hdel("3boNDH3ypRaBX9pc27ZYz049qNP2", "room5"))
# print(r.hget("userhash:1001", "USERID"))


# for item in r.hgetall("Room 5"):
#     print(r.hdel("Room 5", item))
# print(r.hgetall("userhash:1001"))
# p = r.hgetall("userhash:1001")
# print(type(p))
