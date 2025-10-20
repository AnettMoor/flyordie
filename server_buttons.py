import network, socket, time
import machine

# --- LISATUD NUPUD JA LEDID ---
nupp_tagasi = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
nupp_edasi = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_tagasi = machine.Pin(1, machine.Pin.OUT)
led_edasi = machine.Pin(16, machine.Pin.OUT)
# -------------------------------

ssid = "Galaxy S20 FE"
password = "tere12344"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(0.5)

server_ip = "10.169.113.65"  # SERVERI (Pico 1) IP
s = socket.socket()
s.connect((server_ip, 1234))
s.setblocking(False)
print("Ühendatud serveriga:", server_ip)

# --- Nupu olekute jälgimine ---
prev_edasi = 0
prev_tagasi = 0
# -------------------------------

while True:
    # --- Nuppude ja LEDide haldus ---
    if nupp_edasi.value() == 1:
        led_edasi.value(1)
        if prev_edasi == 0:
            s.send(b"BTN_EDASI_ON\n")
            print("Saadetud: BTN_EDASI_ON")
        prev_edasi = 1
    else:
        led_edasi.value(0)
        if prev_edasi == 1:
            s.send(b"BTN_EDASI_OFF\n")
            print("Saadetud: BTN_EDASI_OFF")
        prev_edasi = 0

    if nupp_tagasi.value() == 1:
        led_tagasi.value(1)
        if prev_tagasi == 0:
            s.send(b"BTN_TAGASI_ON\n")
            print("Saadetud: BTN_TAGASI_ON")
        prev_tagasi = 1
    else:
        led_tagasi.value(0)
        if prev_tagasi == 1:
            s.send(b"BTN_TAGASI_OFF\n")
            print("Saadetud: BTN_TAGASI_OFF")
        prev_tagasi = 0
    # --------------------------------

    # --- Serveri vastuse lugemine ---
    try:
        data = s.recv(1024)
        if data:
            print("Server vastas:", data.decode().strip())
    except:
        pass

    time.sleep(0.2)
