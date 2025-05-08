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
        # check length data only 31 byte include checksum
        if not datas or len(datas) > 31:
            print("❌ Invalid data length")
            return None

        checksum_value = self.cal_checksum(datas)
        datas.append(checksum_value)  # add checksum at end
        return datas

    @staticmethod
    def parse_receive_data(data_bytes):
        # check length of received data
        if len(data_bytes) != 17:
            raise ValueError("Invalid packet length")
        
        unpacked = struct.unpack("<IBBBhh5bB", data_bytes)  # unpack with format "<IBBBhh5bB"
        checksum_value = RFComm.cal_checksum(list(data_bytes[:16]))

        # check checksum
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

    def prepare_data_to_send(self, data_bytes):
        # check data to send
        if isinstance(data_bytes, bytearray):
            data_bytes = list(data_bytes)

        packet_with_checksum = self.sync_data(data_bytes)
        if packet_with_checksum is None:
            print("❌ Failed to prepare packet: sync_data() returned None")
            return None

        return bytearray(packet_with_checksum)

    def send(self, data_bytes):
        # check data to send
        packet_with_checksum = self.sync_data(data_bytes)
        if packet_with_checksum is None:
            print("❌ Cannot send: sync_data returned None")
            return False
        packet_bytes = bytearray(packet_with_checksum)
        # print("📡 Packet to send:", list(packet_bytes))

        return self.sendSafe(packet_bytes)

    def sendSafe(self, data_bytes):
        # change to tx role and send
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
        # change to rx role and read
        if self.role != 'RX':
            self.set_rx_role()
            self.role = 'RX'

        received_msg = self.radio.read(17)
        return received_msg

    def isDataAvailable(self):
        # check if data avaolable
        if self.role != 'RX':
            self.set_rx_role()
            self.role = 'RX'
        return self.radio.available()
