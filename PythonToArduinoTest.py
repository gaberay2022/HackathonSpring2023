#Currently only allows basic input from python file to be read by arduino
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # import opencv-python
import numpy as np # import numpy for arrays
import time #import time for delays
import serial #import serial for arduino communication

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(1)

#set up arduino calls on com3 port with correct baud
arduinoData=serial.Serial('com3', 115200)

def returnvalues(value): #function to return integer value that will be read into arduino
    if value == 0:
        return 0 #compost
    if value == 1:
        return 1 #trash
    if value == 2:
        return 2 #recycle
    if value == 3:
        return 3 #people
    
while True:
    while(arduinoData.inWaiting()==0): #while statment to keep video feed going when not recieving arduino values
        cmd="5" #give default state to arduino
        cmd=cmd+'\r' #add delimiter char
        arduinoData.write(cmd.encode()) #send to arduino
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

    cmd="5" #set default state at start when recieving arduino values incase of mulitple inputs in a row
    cmd=cmd+'\r' #add delimieter char
    arduinoData.write(cmd.encode()) #send to arduion
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

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

    dataPacket = arduinoData.readline() #read in arduino values
    dataPacket = str(dataPacket, 'utf-8') #set arduino values to utf-8 string
    dataPacket = dataPacket.strip('\r\n') #delimit
    x=float(dataPacket) #convert floating point number
    print(dataPacket) #print sonor values for distance in debugging
    if not x < 5 and x <= 25: #if equal or less than 25 cm away and greater than 5 cm away 
        values=returnvalues(index) #get value relating to trash shoot to send to arduino
        cmd=f"{values}" #set num value to string in or
        cmd=cmd+'\r' #add delimiter value
        arduinoData.write(cmd.encode()) #send to arduino
        time.sleep(4) #pause python program for delay

camera.release() #close camera access when esc key pressed
cv2.destroyAllWindows() #destroys cv window