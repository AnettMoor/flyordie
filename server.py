import network
import socket
import time
from machine import Pin, PWM

# --- mootorid (picost alates) ---
motor1 = PWM(Pin(28))
motor1.freq(10000) # voib ka proovida 20000 (võib olla smoother control?)

motor2 = PWM(Pin(27))
motor2.freq(10000)

motor3 = PWM(Pin(26))
motor3.freq(10000)

motor4 = PWM(Pin(21)) #KATKINE
motor4.freq(10000)

motor5 = PWM(Pin(18))
motor5.freq(10000)

motor6 = PWM(Pin(14))
motor6.freq(10000)

motor7 = PWM(Pin(17))
motor7.freq(10000)

motor8 = PWM(Pin(16))
motor8.freq(10000)
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

        
            # --- MOOTORITE TÖÖTAMINE VASTAVALT KÄSULE ---
            if msg == "BTN_EDASI_ON": # puldil vajutatakse nuppu otse, siis
                # MOOTOR
                motor1.duty_u16(40000) # mootori kiirus/tööle mootor
                time.sleep(2)        # mitu sek töötab mootor
                motor1.duty_u16(0)    # mootor kinni

                motor5.duty_u16(40000)
                time.sleep(2)  
                motor5.duty_u16(0)
                
            elif msg == "BTN_TAGASI_ON":
                motor2.duty_u16(40000)
                time.sleep(2)  
                motor2.duty_u16(0)

                motor6.duty_u16(40000)
                time.sleep(2)  
                motor6.duty_u16(0)
                
            elif msg == "BTN_VASAKULE_ON":
                motor2.duty_u16(40000)
                time.sleep(2)  
                motor2.duty_u16(0) 

                motor7.duty_u16(40000)
                time.sleep(2)  
                motor7.duty_u16(0)
                
            elif msg == "BTN_PAREMALE_ON":
                motor4.duty_u16(40000)
                time.sleep(2)  
                motor4.duty_u16(0) 

                motor8.duty_u16(40000)
                time.sleep(2)  
                motor8.duty_u16(0)
            # ------------------------------
            conn.send(b"OK\n")
    except:
        pass

    time.sleep(0.1)
