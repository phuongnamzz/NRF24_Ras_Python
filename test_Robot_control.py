from time import sleep
from Robot_control import RFComm
from sshkeyboard import listen_keyboard
import struct

def create_fake_data_without_checksum():
    robot_id = 11223
    status = 1
    axis0, axis1, axis2, axis3 = 50, -200, 300, -199
    buttons = [1] * 17  # 17 buttons

    # packed data with format "<IBhhhh17B"
    packed = struct.pack("<IBhhhh17B", robot_id, status, axis0, axis1, axis2, axis3, *buttons)
    return list(packed)  # return list
parsed_data = []

def press(key):
    print(f"'{key}' pressed")
    if key in ['up', 'w']:
        fake_data = create_fake_data_without_checksum()  # create fake_data
        rf24 = RFComm(channel=64, address=b'11223', rx_pipe_address=b"11223")
        
        if rf24.send(fake_data):
            sleep(0.05)
            if rf24.isDataAvailable():
                data = rf24.read_data()
                if data:
                    try:
                        parsed_data = rf24.parse_receive_data(data)
                        # print("📦 Parsed data:", parsed_data)
                    except ValueError as e:
                        print("❌ Error parsing data:", e)
                else:
                    print("❌ No data received")
            else:
                print("❌ No echo received")

def release(key):
    print(f"'{key}' released")

# listen keyboard
listen_keyboard(
    on_press=press,
    on_release=release,
)
