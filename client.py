import network, socket, time
import machine

nupp_edasi = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
nupp_tagasi = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN)
nupp_vasakule = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
nupp_paremale = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)


ssid = "Galaxy S20 FE"
password = "flyordie"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(0.5)

server_ip = "10.169.113.65" # server ip
s = socket.socket()
s.connect((server_ip, 1234))
s.setblocking(False)
print("Ühendatud serveriga:", server_ip)

prev_edasi = 0
prev_tagasi = 0
prev_vasakule = 0
prev_paremale = 0

while True:
    # edasi
    if nupp_edasi.value() == 1:
        if prev_edasi == 0:
            s.send(b"BTN_EDASI_ON\n")
            print("Saadetud: BTN_EDASI_ON")
        prev_edasi = 1
    else:
        if prev_edasi == 1:
            s.send(b"BTN_EDASI_OFF\n")
            print("Saadetud: BTN_EDASI_OFF")
        prev_edasi = 0

    # tagasi
    if nupp_tagasi.value() == 1:
        if prev_tagasi == 0:
            s.send(b"BTN_TAGASI_ON\n")
            print("Saadetud: BTN_TAGASI_ON")
        prev_tagasi = 1
    else:
        if prev_tagasi == 1:
            s.send(b"BTN_TAGASI_OFF\n")
            print("Saadetud: BTN_TAGASI_OFF")
        prev_tagasi = 0

    # vasakule
    if nupp_vasakule.value() == 1:
        if prev_vasakule == 0:
            s.send(b"BTN_VASAKULE_ON\n")
            print("Saadetud: BTN_VASAKULE_ON")
        prev_vasakule = 1
    else:
        if prev_vasakule == 1:
            s.send(b"BTN_VASAKULE_OFF\n")
            print("Saadetud: BTN_VASAKULE_OFF")
        prev_vasakule = 0

    # paremale
    if nupp_paremale.value() == 1:
        if prev_paremale == 0:
            s.send(b"BTN_PAREMALE_ON\n")
            print("Saadetud: BTN_PAREMALE_ON")
        prev_paremale = 1
    else:
        if prev_paremale == 1:
            s.send(b"BTN_PAREMALE_OFF\n")
            print("Saadetud: BTN_PAREMALE_OFF")
        prev_paremale = 0

    # serveri vastus
    try:
        data = s.recv(1024)
        if data:
            print("Server vastas:", data.decode().strip())
    except:
        pass

    time.sleep(0.2)
