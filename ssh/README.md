-Install package
```bash
pip install paramiko
```
  paramiko can't run on python 2. If there is any error with paramiko, try:
```bash
pip3 install paramiko
python3 ssh.py --table ...
```

-Change key file permission
```bash
chmod 0600 jlf
```

-Run py file  
  new notification:
```bash
python ssh.py --table 1
```
  new image:
```bash
python ssh.py --table 2 --image <image path> --species <0:nothing, 1:squirrel, 2:bird>
```
