try:
    from pirc522 import RFID
    import RPi.GPIO as GPIO
except ImportError as e:
    print("No libs")

import time

KEY_B = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def decode(d):
    return ''.join([chr(x) for x in d])

def decode_number(d):
    return int(decode(d), 16)

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
    util.do_auth(1)
    err, id_block = rdr.read(1)
    if err:
        print("Error", id_block)
        continue
    if decode(id_block).strip() != "CONFIG CARD":
        print("Not a config card")
    util.do_auth(2)
    err, block_one = rdr.read(2)
    if err:
        print("Error", block_one)
        continue

    course_name = decode(block_one[:8])
    course_id = decode_number(block_one[8:12])
    token_a = decode_number(block_one[12:])

    token_b = []

    for block in [4, 5, 6, 8]:
        util.do_auth(block)
        err, data = rdr.read(block)
        if err:
            print("Error", data)
            continue
        token_b.append(decode(data))
    token = f"{token_a}~{''.join(token_b)}"

    print(course_name, course_id)
    print(token)

    print("Done.")
    time.sleep(3)

