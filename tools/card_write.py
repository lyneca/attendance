# Note: This script is _only_ for use in legitimate educational applications.

from pirc522 import RFID
import RPi.GPIO as GPIO
import time

KEY_A = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
KEY_B = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
sector = int(input("Enter Sector: "))
new_data = f'{input("Enter data: "): <16}'
new_data = [ord(x) for x in new_data]

def print_out(d):
    print(''.join([chr(x) for x in d]))

rdr = RFID()

util = rdr.util()

while True:
    rdr.wait_for_tag()
    (e, tag_type) = rdr.request()
    if e: continue
    (e, uid) = rdr.anticoll()
    if e: continue
    print("UID:", uid)
    rdr.select_tag(uid)
    print("Authing...")
    rdr.card_auth(rdr.auth_b, sector, KEY_B, uid)
    print("Reading...")
    data = rdr.read(sector)
    print("  Error:", data[0])
    print_out(data[1])
    print("Writing...")
    rdr.write(sector, new_data)
    print("Written. Current data:")
    data = rdr.read(sector)
    print("  Error:", data[0])
    print_out(data[1])
    time.sleep(1)

