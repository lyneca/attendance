try:
    from pirc522 import RFID
    import RPi.GPIO as GPIO
except ImportError as e:
    print("No libs")

import time

KEY_B = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def hexize(string):
    return [ord(x) for x in string]

with open("/home/pi/usyd_key") as key_file:
    key = [ord(x) for x in key_file.read().strip()]

course_code = input("Enter the course code: ")
course_id = hex(int(input("Enter the course ID: ")))[2:]
token = input("Enter your token: ")

token_a, token_b = token.split('~')

token_a = hex(int(token_a))[2:]

blocks = [
    None,
    hexize(f'{"CONFIG CARD": <16}'),
    hexize(f'{course_code: >8}{course_id:0>4}{token_a:0>4}'),
    key + [None,None,None,None,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
    hexize(token_b[:16]),
    hexize(token_b[16:32]),
    hexize(token_b[32:48]),
    key + [None,None,None,None,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
    hexize(token_b[48:]),
    None,
    None,
    key + [None,None,None,None,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
]

print(blocks)

def print_out(d):
    print(''.join([chr(x) for x in d]))

rdr = RFID()

util = rdr.util()
util.debug = False

while True:
    rdr.wait_for_tag()
    (e, tag_type) = rdr.request()
    if e: continue
    (e, uid) = rdr.anticoll()
    if e: continue
    print("UID:", uid)
    util.set_tag(uid)
    util.auth(rdr.auth_b, KEY_B)
    for sector in range(len(blocks)):
        if blocks[sector] is not None:
            #  print(f"Authing sector {sector + 1} of {len(blocks)}...")
            #  print(err)
            print(f"Writing sector {sector + 1} of {len(blocks)}...")
            err = util.rewrite(sector, blocks[sector])
            if err:
                print("Error:", err)
    print("Done.")
    time.sleep(3)
