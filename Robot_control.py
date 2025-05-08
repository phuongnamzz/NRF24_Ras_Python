
from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS
import struct

class RFComm:
    def __init__(self, channel, address, ce_pin=22, csn_pin=0, role="RX", rx_pipe_address=None):
        self.radio = RF24(ce_pin, csn_pin)
        if not self.radio.begin():
            raise RuntimeError("❌ NRF24 initialization failed!")

        self.rx_pipe_address = rx_pipe_address or address
        self.radio.setPALevel(RF24_PA_MAX)
        self.radio.setDataRate(RF24_250KBPS)
        self.radio.setRetries(5, 15)
        self.address = address
        self.role = role.upper()
        self.radio.setChannel(channel)

        if self.role == "TX":
            self.set_tx_role()
        elif self.role == "RX":
            self.set_rx_role()
        else:
            raise ValueError("❌ Role must be 'TX' or 'RX'")

    def set_tx_role(self):
        self.radio.openWritingPipe(self.address)
        self.radio.stopListening()

    def set_rx_role(self):
        self.radio.openReadingPipe(1, self.rx_pipe_address)
        self.radio.startListening()

    @staticmethod
    def cal_checksum(datas):
        if not datas or not isinstance(datas, list):
            raise ValueError("Input must be a non-empty list")
        return sum(datas) & 0xFF

    def sync_data(self, datas):
        if not datas or len(datas) > 31:  # chỉ được tối đa 32 byte, 1 byte dành cho checksum
            print("❌ Invalid data length")
            return None

        checksum_value = self.cal_checksum(datas)
        datas.append(checksum_value)
        # print(f"📦 Data (with checksum): {datas}")

        return datas

    @staticmethod
    def parse_receive_data(data_bytes):
        if len(data_bytes) != 17:
            raise ValueError("Invalid packet length")
        
        unpacked = struct.unpack("<IBBBhh5bB", data_bytes)
        checksum_value = RFComm.cal_checksum(list(data_bytes[:16]))

        # print(f"Checksum (calculated): {checksum_value}")
        # print(f"Checksum (packet): {unpacked[11]}")

        if unpacked[11] != checksum_value:
            raise ValueError("Checksum mismatch")

        return {
            "robot_id": unpacked[0],
            "status": unpacked[1],
            "error": unpacked[2],
            "battery": unpacked[3],
            "L_wheel": unpacked[4],
            "R_wheel": unpacked[5],
            "weapon": list(unpacked[6:11]),
            "checksum": unpacked[11]
        }

    def send(self, data_bytes: bytearray):
        if self.role != 'TX':
            self.set_tx_role()
            self.role = 'TX'

        print(f"📡 Sending bytes: {list(data_bytes)}")
        success = self.radio.write(data_bytes)

        if success:
            print("✅ Sent successfully!")
        else:
            print("❌ Send failed!")

        self.set_rx_role()
        self.role = 'RX'

        return success

    def read_data(self):
        if self.role != 'RX':
            self.set_rx_role()
            self.role = 'RX'

        received_msg = self.radio.read(17)  
        # print(f"📥 Raw bytes received: {list(received_msg)}")

        return received_msg


    def isDataAvailable(self):
        if self.role != 'RX':
            self.set_rx_role()
            self.role = 'RX'
        return self.radio.available()


