import serial
import time

ser = serial.Serial('COM3', baudrate=230400, timeout=1)

def send_command(command):
    ser.write((command + '\r\n').encode())  # Send command
    time.sleep(0.1)  # Wait for the command to be executed
    response = ser.read_all().decode()  # Read response
    return response


def SendCommandToFlipper(command):
    global ser
    if not ser.isOpen():
        ser = serial.Serial('COM3', baudrate=230400, timeout=1)
    response = send_command(command)
    ser.close()
    return response

def SendColorToFlipper(color):
    command = 'ir universal Remote2 ' + color
    return SendCommandToFlipper(command)



def CheckButton():
    global ser
    if not ser.isOpen():
        ser = serial.Serial('COM3', baudrate=230400, timeout=1)
        send_command('gpio mode PA7 0')
    response = send_command('gpio read PA7')
    if response.__contains__('PA7 <= 1'):
        ser.close()
        return 1
    if response.__contains__('Pin PA7 <= 0'):
        return 0
    ser.close()
    return -1

SendColorToFlipper('Red')
print(CheckButton())