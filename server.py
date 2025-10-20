import network
import socket
import time
import machine

# --- LEDid serveril (GP1 ja GP16 näiteks) ---
led_tagasi = machine.Pin(15, machine.Pin.OUT)
led_edasi = machine.Pin(19, machine.Pin.OUT)
# --------------------------------------------

ssid = "Galaxy S20 FE"
password = "flyordie"

# --- WiFi seadistus ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Ühendan WiFi-ga...")
while not wlan.isconnected():
    time.sleep(0.5)

ip = wlan.ifconfig()[0]
print("WiFi ühendatud! IP aadress:", ip)

# --- Socket server ---
s = socket.socket()
s.bind(('0.0.0.0', 1234))
s.listen(1)

print("Ootan klienti...")
conn, addr = s.accept()
print("Klient ühendatud:", addr)

# Non-blocking mode so loop doesn’t freeze
conn.setblocking(False)

while True:
    try:
        data = conn.recv(1024)
        if data:
            msg = data.decode().strip()
            print("Sain:", msg)

            # --- LED reaktsioon käsule ---
            if msg == "BTN_EDASI_ON":
                led_edasi.value(1)
            elif msg == "BTN_EDASI_OFF":
                led_edasi.value(0)
            elif msg == "BTN_TAGASI_ON":
                led_tagasi.value(1)
            elif msg == "BTN_TAGASI_OFF":
                led_tagasi.value(0)
            # ------------------------------

            conn.send(b"OK\n")
    except:
        pass

    time.sleep(0.1)
