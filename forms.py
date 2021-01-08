import redis
import os
from datetime import date


redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
r = redis.StrictRedis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

user = {"Name": "Pradeep", "Company": "SCTL", "Address": "Mumbai", "Location": "RCP"}

#
# r.hset("ROOM_ID", mapping={"USERI5": "DATE_JOINED", "USERI6": "DATE_JOINED"})
# print(r.hset("userhash:1001", mapping={"USERI5": "DATE_JOINED"}))

print(r.hgetall("Room 5"))
# #
print(r.hexists("3boNDH3ypRaBX9pc27ZYz049qNP2", "room5"))


# print(r.hget("userhash:1001", "USERID"))

#
# for item in r.hgetall("Room 5"):
#     print(r.hdel("Room 5", item))
# print(r.hgetall("userhash:1001"))
# p = r.hgetall("userhash:1001")
# print(type(p))