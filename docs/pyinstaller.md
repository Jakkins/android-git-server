# pyinstaller

## icon 

https://www.xiconeditor.com/

if problem:
1. Enable Hidden Items
2. Go to C:\Users\User\AppData\Local\Microsoft\Windows\Explorer
   1. Select all files that begin with `iconcache` and `thumbcache` and delete all these files
3. Go to C:\Users\user\AppData\Local and delete `IconCache.db`

```bash
pip install --upgrade pip
pip install pyinstaller
pyinstaller.exe --onefile -i='.\ags.ico' ags.py
```

```bash
C:\Users\username\AppData\Local\Programs\Python\Python311\python.exe -m pip install --upgrade pip
```