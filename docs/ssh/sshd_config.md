```bash
PrintMotd yes
Subsystem sftp /data/data/com.termux/files/usr/libexec/sftp-server
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowTcpForwarding no
X11Forwarding no
```

- PrintMotd: show message to user when log into an ssh session
- Subsystem: where to find the program to manage file exchange with ssh
- the others are secure configuration