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

# not a solution but still usable

The thing is:

- when you can't connect to internet you can usb tethering with the smartphone
- when you can connect to internet, just connect also the smartphone to the LAN
- you can do wifi hotspot with another cell and connect to it to bypass this problem