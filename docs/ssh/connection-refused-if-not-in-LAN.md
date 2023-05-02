# ssh connection refused if not in lan

> connection is always towards the localhost

```bash
adb forward tcp:8022 tcp:8022
adb forward --list
# aabb1122 tcp:8022 tcp:8022
nmap.exe localhost
# 8022/tcp  open  oa-system
ssh.exe -vvv -i C:\Users\samuele.plescia\.ssh\ags-key -p 8022 localhost
# ssh: connect to host aabb1122 port 8022: Connection refused
```
