# ssh config

add in `C:\Users\username\.ssh\config`

```txt
Host localhost
  HostName localhost
  User ags
  IdentityFile C:\pat\to\ags-key
```

test with:

```bash
ssh -p 8022 -Tv localhost
```
