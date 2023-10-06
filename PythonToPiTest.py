#Currently only allows basic input from python file to be read on pi

import trace
import tensorflow #NEED TO INSTALL THESE
import tflite #NEED TO INSTALL THESE

from gpiozero import LED #This is for the pins on the PI
from gpiozero import DistanceSensor

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # import opencv-python
import numpy as np # import numpy for arrays
import time #import time for delays
import serial #import serial for arduino communication
import os

# Setting up virtual environ for Camera input to function
os.system('Xvfb :0 -screen 0 1024x768x24 &')
os.environ['DISPLAY'] = ':0'

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0) #Might need to swap this to something connecting to the PI

def returnvalues(value): #function to return integer value that will be read into arduino
    if value == 0:
        return 0 #compost
    if value == 1:
        return 1 #trash
    if value == 2:
        return 2 #recycle
    if value == 3:
        return 3 #people


#https://www.ics.com/blog/control-raspberry-pi-gpio-pins-python is where I found info on gpiozero
#setup the LEDs on the pins (need to get the pin numbers from the pi first)
Trash_LED = LED(17)
Recycle_LED = LED(27)
Compost_LED = LED(22)

#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
Ultrasonic = DistanceSensor(echo = 5, trigger = 6) #Those two are two different pins
#PIN NUMBERS ARE TEMPORARY

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # # Normalize the image array
    image = (image / 127.5) - 1

    # # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    Sensor_distance = Ultrasonic.distance # Keep track os sensor distance

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    print("Distance from sensor:",Sensor_distance)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

    if 0.05 < Sensor_distance <= 0.25: #if equal or less than 25 cm away and greater than 5 cm away
        values = returnvalues(index) #get value relating to trash shoot to send to arduino
        if values == 0:
            Compost_LED.on()
            Trash_LED.off()
            Recycle_LED.off()
        elif values == 1:
            Compost_LED.off()
            Trash_LED.on()
            Recycle_LED.off()
        elif values == 2:
            Compost_LED.off()
            Trash_LED.off()
            Recycle_LED.on()
        else:
            Trash_LED.off()
            Recycle_LED.off()
            Compost_LED.off()

        time.sleep(3) #pause python program for delay

    else:
        Trash_LED.off()
        Recycle_LED.off()
        Compost_LED.off()

camera.release() #close camera access when esc key pressed
cv2.destroyAllWindows() #destroys cv window
