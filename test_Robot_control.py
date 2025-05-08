from time import sleep
from Robot_control import RFComm
from sshkeyboard import listen_keyboard
import struct
import random

import struct


def create_fake_data_without_checksum():
    robot_id = 11223
    status = 1
    axis0, axis1, axis2, axis3 = 100, -200, 300, -400
    buttons = [1]*17  


    packed = struct.pack("<IBhhhh17B", robot_id, status, axis0, axis1, axis2, axis3, *buttons)
    return list(packed)  



fake_data = create_fake_data_without_checksum()
# print("fake data", list(fake_data))

rf24 = RFComm(channel=64, address=b'11223', rx_pipe_address=b"11223")

packet_with_checksum = rf24.sync_data(fake_data)
# print("sync data",packet_with_checksum)
packet_bytes = bytearray(packet_with_checksum)
parsed_data = []
def press(key):
    print(f"'{key}' pressed")
    if key in ['up', 'w']:
        if rf24.send(packet_bytes):
            sleep(0.05)  # 
            if rf24.isDataAvailable():
                data = rf24.read_data()
                # print(type(data))
                if data:
                    try:
                        parsed_data = rf24.parse_receive_data(data)
                        print("📦 Parsed data:", parsed_data)
                    except ValueError as e:
                        print("❌ Error parsing data:", e)
                else:
                    print("❌ No data received")
                # print("🔁 Echo received:", data)
            else:
                print("❌ No echo received")
    
def release(key):
    print(f"'{key}' released")

listen_keyboard(
    on_press=press,
    on_release=release,
)
