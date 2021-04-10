
import numpy as np
import paramiko
import pyimgur
from picamera import PiCamera
from time import sleep


def insert_data(table, species=0):
    try:
        if table == 1:
            command = './insert_notification.sh'
        elif table == 2:
            # upload image to imgur
            CLIENT_ID = '0c214ab9446e86e'
            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image("pic.jpg", title="pic")
            url = uploaded_image.link
            species = str(species)
            # url = "https://images.unsplash.com/photo-1480044965905-02098d419e96?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
            command = './insert_image.sh "' + url + '" ' + species
        else:
            command = 'ls'

        # ssh to cPanel
        key = paramiko.RSAKey.from_private_key_file('xyt', password='SSPBF_ece445')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("web.illinois.edu", username="birdfeeder", look_for_keys=False, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh.close()
        del ssh, stdin, stdout, stderr

    except:
        print("unable to insert data")

def object_detection(threshold=0.5, modeldir='BirdSquirrelRaccoon_TFLite_model', graph='detect.tflite', labels='labelmap.txt'):
    import cv2
    import os
    from tflite_runtime.interpreter import Interpreter

    camera = PiCamera()
    camera.start_preview()
    # sleep(1)
    camera.capture('pic.jpg')
    camera.stop_preview()
    image = 'pic.jpg'
    # Get path to current working directory
    CWD_PATH = os.getcwd()

    PATH_TO_IMAGES = os.path.join(CWD_PATH,image)

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH,modeldir,graph)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,modeldir,labels)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    # Load the Tensorflow Lite model.
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Load image and resize to expected shape [1xHxWx3]
    image = cv2.imread(PATH_TO_IMAGES)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape 
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

    signal = 0
    for i in range(len(scores)):
        if (scores[i] >= threshold) and (scores[i] <= 1.0) and signal != 1:
            if classes[i] == 0:
                signal = 2
            elif classes[i] == 1:
                signal = 1
    if signal == 1:
        print("Squirrel!!!!!!!")
    elif signal == 2:
        print("Bird!!!!!!!!")
    else:
        print("Nothing!!!!!!!!!!")
    
    return signal