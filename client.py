import machine
import network
import socket
import time

# --- Nupud ja LEDid ---
nupp_tagasi = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_tagasi = machine.Pin(1, machine.Pin.OUT)

nupp_edasi = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_edasi = machine.Pin(16, machine.Pin.OUT)

nupp_vasakule = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_vasakule = machine.Pin(15, machine.Pin.OUT)

nupp_paremale = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_paremale = machine.Pin(18, machine.Pin.OUT)

# --- Mootorid (ühendatud läbi transistoride või draiveri) ---
mootor_edasi_vasak = machine.Pin(2, machine.Pin.OUT)
mootor_edasi_parem = machine.Pin(3, machine.Pin.OUT)
mootor_tagasi_vasak = machine.Pin(4, machine.Pin.OUT)
mootor_tagasi_parem = machine.Pin(5, machine.Pin.OUT)

# --- Mootori parameetrid ---
KV = 19000       # pööret volt/sek
PINGE = 3.7      # toitepinge
porded_sekundis = KV * PINGE / 60  # RPM → RPS (pööret sekundis)

def keera_mootorit(mootor, poorded):
    """Käivitab ühe mootori määratud arv pöördeid"""
    kestus = poorded / porded_sekundis
    print("Mootor teeb", poorded, "pööret (~", round(kestus, 4), "sekundit )")
    mootor.value(1)
    time.sleep(kestus)
    mootor.value(0)
    print("Mootor peatatud.")

# --- WiFi ühendus ---
ssid = "Galaxy S20 FE"
password = "flyordie"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(0.5)

server_ip = "10.169.113.65"
s = socket.socket()
s.connect((server_ip, 1234))
s.setblocking(False)
print("Ühendatud serveriga:", server_ip)

# --- Muutujad eelmise seisundi jälgimiseks ---
prev_edasi = prev_tagasi = prev_vasakule = prev_paremale = 0

# --- Peatsükliline töö ---
while True:
    # --- Edasi ---
    if nupp_edasi.value() == 1:
        led_edasi.value(1)
        if prev_edasi == 0:
            s.send(b"BTN_EDASI_ON\n")
            print("Saadetud: BTN_EDASI_ON")
            # Käivita mõlemad esimesed mootorid 50 pööret
            keera_mootorit(mootor_edasi_vasak, 50)
            keera_mootorit(mootor_edasi_parem, 50)
        prev_edasi = 1
    else:
        led_edasi.value(0)
        if prev_edasi == 1:
            s.send(b"BTN_EDASI_OFF\n")
            print("Saadetud: BTN_EDASI_OFF")
        prev_edasi = 0

    # --- Tagasi ---
    if nupp_tagasi.value() == 1:
        led_tagasi.value(1)
        if prev_tagasi == 0:
            s.send(b"BTN_TAGASI_ON\n")
            print("Saadetud: BTN_TAGASI_ON")
            keera_mootorit(mootor_tagasi_vasak, 50)
            keera_mootorit(mootor_tagasi_parem, 50)
        prev_tagasi = 1
    else:
        led_tagasi.value(0)
        if prev_tagasi == 1:
            s.send(b"BTN_TAGASI_OFF\n")
            print("Saadetud: BTN_TAGASI_OFF")
        prev_tagasi = 0

    # --- Vasakule ---
    if nupp_vasakule.value() == 1:
        led_vasakule.value(1)
        if prev_vasakule == 0:
            s.send(b"BTN_VASAKULE_ON\n")
            print("Saadetud: BTN_VASAKULE_ON")
            # vasakule pööramiseks käivitame vastavad mootorid
            keera_mootorit(mootor_edasi_parem, 30)
            keera_mootorit(mootor_tagasi_vasak, 30)
        prev_vasakule = 1
    else:
        led_vasakule.value(0)
        if prev_vasakule == 1:
            s.send(b"BTN_VASAKULE_OFF\n")
            print("Saadetud: BTN_VASAKULE_OFF")
        prev_vasakule = 0

    # --- Paremale ---
    if nupp_paremale.value() == 1:
        led_paremale.value(1)
        if prev_paremale == 0:
            s.send(b"BTN_PAREMALE_ON\n")
            print("Saadetud: BTN_PAREMALE_ON")
            keera_mootorit(mootor_edasi_vasak, 30)
            keera_mootorit(mootor_tagasi_parem, 30)
        prev_paremale = 1
    else:
        led_paremale.value(0)
        if prev_paremale == 1:
            s.send(b"BTN_PAREMALE_OFF\n")
            print("Saadetud: BTN_PAREMALE_OFF")
        prev_paremale = 0

    # --- Serveri vastus ---
    try:
        data = s.recv(1024)
        if data:
            print("Server vastas:", data.decode().strip())
    except:
        pass

    time.sleep(0.1)
