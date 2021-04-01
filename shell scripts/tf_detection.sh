#!/bin/bash
cd ECE445/tflite1
source tflite1-env/bin/activate
raspistill -o pic.jpg  -t 200
python3 TFLite_image.py --modeldir BirdSquirrelRaccoon_TFLite_model/ --image pic.jpg