#!/usr/bin/python3

import redis

for x in range(2512):
    conn = redis.Connection(host="10.20.1.71", port=1339, socket_timeout=2)
    conn.connect()
    conn.send_command("ping")
    print(conn.read_response())


