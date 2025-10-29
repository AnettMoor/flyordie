import network
import socket
import time
from machine import Pin, PWM

# --- mootorid ---
motor1 = PWM(Pin(26))
motor1.freq(10000)

motor2 = PWM(Pin(28))
motor2.freq(10000)

motor3 = PWM(Pin(27))  # ei tööta hetkel, vasak
motor3.freq(10000)

motor4 = PWM(Pin(21)) # ei tööta hetkel, vasak
motor4.freq(10000)
# --------------------------------------------


# --- WiFi seadistus ---
ssid = "Galaxy S20 FE"
password = "flyordie"

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
            if msg == "BTN_EDASI":
                # MOOTOR    
                motor1.duty_u16(40000) # mootori kiirus/tööle mootor
                time.sleep(2)        # mitu sek töötab mootor
                motor1.duty_u16(0)    # mootor kinni
            elif msg == "BTN_TAGASI":
                motor2.duty_u16(40000)
                time.sleep(2)  
                motor2.duty_u16(0)
            elif msg == "BTN_VASAKULE":
                motor2.duty_u16(40000)
                time.sleep(2)  
                motor2.duty_u16(0) 
            elif msg == "BTN_PAREMALE":
                motor4.duty_u16(40000)
                time.sleep(2)  
                motor4.duty_u16(0) 
            # ------------------------------
            conn.send(b"OK\n")
    except:
        pass

    time.sleep(0.1)
