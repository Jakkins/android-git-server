# kex_exchange_identification: Connection closed by remote host

https://superuser.com/questions/1782355/termux-ssh-connection-over-usb-c-result-in-connection-closed-by-remote-host

> connection is always towards the localhost

```bash
adb forward tcp:8022 tcp:8022
adb forward --list
# aabb1122 tcp:8022 tcp:8022
nmap.exe localhost
# 8022/tcp  open  oa-system
ssh.exe -vvv -i C:\Users\username\.ssh\ags-key -p 8022 localhost
# ssh: connect to host aabb1122 port 8022: Connection refused
```

```bash
sshd -ddd
```