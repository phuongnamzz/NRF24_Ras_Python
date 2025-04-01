from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS
import time

radio = RF24(22, 0)  # CE=4, CSN=5 (Giống Arduino)

if not radio.begin():
    print("NRF24 init failed")
    exit()

# ⚡ Tăng công suất phát & đặt tốc độ dữ liệu khớp với Arduino
radio.setAutoAck(1)
radio.setPALevel(RF24_PA_MAX)  # Mạnh nhất
radio.setDataRate(RF24_250KBPS)  # Để xa & ổn định hơn
radio.setRetries(5, 15)  # 5 lần thử, cách nhau 15*250us
radio.openWritingPipe(b"00001")  # Địa chỉ phải khớp với Arduino
radio.stopListening()

while True:
    msg = b"ON"
    print("📤 Đang gửi:", msg.decode())

    if radio.write(msg):
        print(" Gửi thành công!")
    else:
        print(" Gửi thất bại!")

    time.sleep(1)
    msg = b"OFF"
    print("📤 Đang gửi:", msg.decode())

    if radio.write(msg):
        print(" Gửi thành công!")
    else:
        print(" Gửi thất bại!")
    time.sleep(1)
