import machine # type: ignore
import time
import socket
import network # type: ignore

# Global variables
countdown_value = 15  # Valor por defecto
running = False
sleep_time = 200

# Configuración de la red
ssid = 'FCCARMEN'
password = '1101760558velez'

# Pins assignment
#displayUnidades_pins = [35,36,37,38,39,40,41,42]  # Pines para el primer display 7
displayUnidades_pins = [21,13,11,46]
#displayDecenas_pins = [18,17,19,20,3,14,21,46,10,11,13,12]  # 12
P_objects = []
button_pin = 4  # Pin para el botón

def setup_display(pins):
    for pin in pins:
        Pin_obj = machine.Pin(pin, machine.Pin.OUT)
        P_objects.append(Pin_obj)

# Button setup
def setup_button(btn_pin):
    button = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return button

def display_number(display_pins, number):
    digit_map = [
        0b0000,  # 0
        0b0001,  # 1
        0b0010,  # 2
        0b0011,  # 3
        0b0100,  # 4
        0b0101,  # 5
        0b0110,  # 6
        0b0111,  # 7
        0b1000,  # 8
        0b1001   # 9
    ]
    if 0 <= number < 100:
        tens = number // 10
        ones = number % 10
        # Mostrar decenas
        # for i in range(0, len(P_objects)):
        #     machine.Pin(display_pins[i], machine.Pin.OUT).value((digit_map[tens] >> i) & 1)
        # time.sleep(0.005)  # Tiempo para visualizar
        # Mostrar unidades
        for i in range(len(P_objects)):
            machine.Pin(display_pins[i], machine.Pin.OUT).value((digit_map[ones] >> i) & 1)
        #time.sleep(1)  # Tiempo para visualizar

def countdown(seconds):
    global running
    running = True
    while seconds >= 0 and running:
        display_number(displayUnidades_pins, seconds)
        #display_number(display2_pins, seconds)
        time.sleep(1)
        seconds -= 1
    running = False

# Configuración de la red
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ipconfig('addr4'))

# Servidor para recibir el valor de la cuenta regresiva
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Servidor escuchando en', addr)
    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Solicitud:', request)

        # Extraer el valor de la cuenta regresiva
        try:
            if 'value=' in request:
                value = int(request.split('value=')[1].split(' ')[0])
                global countdown_value
                countdown_value = max(0, min(99, value))  # Limitar entre 0 y 99
        except Exception as e:
            print('Error al obtener el valor:', e)

        # Responder al cliente
        cl.send(b'HTTP/1.0 200 OK\r\nContent-type:text/html\r\n\r\n')
        cl.send(b'<html><body><h1>Cuenta Regresiva</h1>')
        cl.send(b'<form action="/"><input type="text" name="value"><input type="submit" value="Enviar"></form>')
        cl.send(b'</body></html>')
        cl.close()
    
#GENERAL SETTINGS
setup_display(displayUnidades_pins)
button=setup_button(button_pin)
countdown(countdown_value)
connect_wifi()
start_server()



while(True):
    if not button.value():  # Si el botón es presionado
            if not running:  # Solo iniciar si no está en marcha
                countdown(countdown_value)
    time.sleep(0.1)
    for pin in range(0,len(displayUnidades_pins)):
        P_objects[pin].value(1)
    print("ON")
    time.sleep_ms(sleep_time)
    
    for pin in range(0,len(displayUnidades_pins)):
        P_objects[pin].value(0)
    print("OFF")
    time.sleep_ms(sleep_time)
    

# from machine import Pin

# for i in range(0, 60):
#     try:
#         p = Pin(i, Pin.OUT)
#         print(f'Pin {i} configurado correctamente.')
#     except ValueError:
#         print(f'Pin {i} no es válido.')


for i in range(0, len(displayUnidades_pins)):
    print(P_objects[i].value())