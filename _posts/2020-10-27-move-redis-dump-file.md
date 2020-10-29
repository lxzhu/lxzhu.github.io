---
title: Move redis dump file
tags: [redis]
---

Today, redis service in development env got problem. The reason was disk was full. I moved dump file to another disk which has space.

1. shutdown redis service. I killed it actually. Redis rejected to shutdown itself because it failed to saving file to DB.
1. create redis directory on another disk, grant permission to user "redis"
1. change /etc/redis/redis.conf to point "dir" to new directory.
1. change redis.service file (/lib/systemd/system/redis-server.services on my redis server) to add the directory to ReadWriteDirectories
1. run systemctl daemon-reload
1. start redis service
