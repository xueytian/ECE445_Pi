import paramiko
import argparse
import requests, json
import pyimgur

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, help='path to the image')
parser.add_argument('--species', type=int, help='0 : nothing, 1 : squirrel, 2 : bird')
parser.add_argument('--table', type=int, help='1 : food, 2 : pic', required=True)
args = parser.parse_args()

table = args.table

if table == 1:
    command = './insert_notification.sh'
elif table == 2:
    # upload image to imgur
    CLIENT_ID = '0c214ab9446e86e'
    PATH = 'pic.jpg'
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="pic")
    url = uploaded_image.link
    species = str(args.species)
    command = './insert_image.sh "' + url + '" ' + species
else:
    command = 'ls'

# ssh to cPanel
key = paramiko.RSAKey.from_private_key_file('jlf', password='SSPBF_ece445')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("web.illinois.edu", username="birdfeeder", look_for_keys=False, pkey=key)
stdin, stdout, stderr = ssh.exec_command(command)
ssh.close()
del ssh, stdin, stdout, stderr