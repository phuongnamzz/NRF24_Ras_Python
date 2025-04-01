


from pyrf24 import RF24, RF24_PA_MAX, RF24_250KBPS

radio = RF24(22, 0)  # CE=4, CSN=5

if not radio.begin():
    print("NRF24 init failed")
    exit()

radio.setPALevel(RF24_PA_MAX)
radio.setDataRate(RF24_250KBPS)
radio.openReadingPipe(0, b"00001")
radio.startListening()

print("🔄 Đang lắng nghe...")

while True:
    if radio.available():
        msg = radio.read(32)
        print("📥 Nhận được:", msg.decode(errors="ignore"))

