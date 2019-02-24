# Redis Debug Steps

1. Checked for status of redis using either one of command below

```
service redis status
systemctl status redis.service
```

2. Checked for logs in /var/log directory. Open /etc/redis/redis.conf and find the logging directory and file in "logfile" option.

3. Looked for file and file was not present.

4. Tried to change the logging mode to debug which was in notice earlier to get more informationon logs but that too didnt even create logfile.

5. Then tried to change logfile location to /tmp/redis.log and restarted the service it worked.

6. Then came into conclusion as logfile option is the issue and then fixed it.

## Issue

Logfile mentioned in redis.conf was the problem. The directory which was mentioned was not able to access by service which was running under redis user.

## Fixes

1. Point logfile to /tmp or common directory by giving full access to all user.

2. Point some file like /var/log/redis.log and give read-write permission and ownership to redis user so it will be able to access the file.

3. Simply make service to write to standar output by giving "" 

After doing any one step restart the service and check for the status

```
service redis restart
systemctl restart redis.servcie
```

## Note

Going with fix to 2 is the better solution and I have done that.