## run a script when bootup
1. Make sure to create the shell script in the pi folder, also copy the key file to the pi folder as well. 
```bash
$cd ~
```
2. The shell script 
```bash
#!/bin/bash
cd ECE445/tflite1
source tflite1-env/bin/activate
python3 <file path (the python file we want to run all the time)>
```
3. make the script executable
```bash
sudo chmod +x <filename>.sh
```
4. open .bashrc
```bash
sudo nano .bashrc
```
5. scroll down to the bottom and add
```bash
./<filename>.sh
```
6. save and exit
```bash
Ctrl + X, Y, Enter
```
7. reboot
