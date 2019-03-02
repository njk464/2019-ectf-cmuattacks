from tqdm import tqdm
import sys
import bcrypt
import argparse
import signal
from threading import Thread, Event

parser = argparse.ArgumentParser(description='Brute force cracking of hashes for the MITRE eCTF')
parser.add_argument('--username', metavar='username',
                    nargs='?', help='the username', default="No username provided")
parser.add_argument('--bcrypt_hash', default=None, nargs='?',
                    metavar='bcrypt_hash', help='The bcrypt hash')
parser.add_argument('--start', type=int, default=0, help='The starting pin')
parser.add_argument('--num-threads', type=int, default=1, help="The number of threads")

args = parser.parse_args()

args.bcrypt_hash
starting_location = args.start
pin_range = 100000000
username = args.username
pin_length = 8
hash = None
crack_algorithm = None
num_threads = args.num_threads

def crack_bcrypt(username, pin, bcrypt_hash):
    return bcrypt.checkpw(pin.encode("utf-8"), bcrypt_hash.encode("utf-8"))

if args.bcrypt_hash:
    hash = args.bcrypt_hash
    crack_algorithm = crack_bcrypt



if not crack_algorithm:
    print("No algorithm selected")
    exit(0)

entry_found = False
final_pin = None

def run_cracker(username, starting_location, pin_range):
    global entry_found, final_pin, crack_algorithm
    for i in tqdm(range(starting_location, pin_range)):
        if entry_found:
            break

        pin = max(pin_length - len(str(i)), 0)*"0" + str(i)

        if crack_algorithm(username, pin, hash):
            entry_found = True
            final_pin = pin
            break

def sig_handler(signum, frame):
    global entry_found
    entry_found = True

signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

thread_list = []
start = starting_location
num_cracks = (pin_range - starting_location) // num_threads
for i in range(num_threads):
    top = (i+1)*num_cracks
    if i+1 == num_threads:
        top = pin_range
    thread_list.append(Thread(target=run_cracker,
                              args=(username, i*num_cracks, top)))

print("Starting to crack hashes")
for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(num_threads*"\n")
print("Successful crack!")
print("Username: {0}".format(username))
print("PIN: {0}".format(final_pin))
