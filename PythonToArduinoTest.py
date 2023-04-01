#Currently only allows basic input from python file to be read by arduino

import serial
arduinoData=serial.Serial('com3', 115200)

while True:
    cmd=input()
    cmd=cmd+'\r'
    arduinoData.write(cmd.encode())
