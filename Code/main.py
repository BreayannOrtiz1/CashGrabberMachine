import machine # type: ignore
import time


# GLOBAL VARIABLES

countdownValue = 31  # Default value
running = False
sleep_time = 200    #Sleep time between states
debugTime = 300


# PINS ASSIGNMENT

displayUnidadesPins = [11,12,13,14]  # Pins for display 7 seg
displayDecenasPins = [17,18,21,46]  #19 and 20 doesnt works
displayDecenasPins_ctl = 3 
pinsObjectsU = []  #List for storange pin objects
pinsObjectsD = []
pinsObjectsD_ctl = []
pinTurbine = 8
pinExtractor = 9
pinLigth = 10

pinDoorSen = 4
pinButton = 5

#FUNCTIONS

def setupDisplayU(pins):
    for pin in pins:
        Pin_obj = machine.Pin(pin, machine.Pin.OUT)
        pinsObjectsU.append(Pin_obj)
    for pin in pinsObjectsU:
        pin.value(0)
        

def setupDisplayD(pins):
    pinsObjectsD_ctl.append(machine.Pin(displayDecenasPins_ctl, machine.Pin.OUT))
    pinsObjectsD_ctl[0].value(1)    #Display tens-zero at beginig
    for pin in pins:
        Pin_obj = machine.Pin(pin, machine.Pin.OUT)
        pinsObjectsD.append(Pin_obj)
    for pin in pinsObjectsD:
        pin.value(0)
    

def setupOutput(pin):
    objReturn = machine.Pin(pin, machine.Pin.OUT)
    return objReturn

def setupInput(btn_pin):
    button = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return button

def displayNumber(displayTensPins, displayUnitsPins, number):
    print("CountDown: "+str(number))
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
        if(tens<1):
            pinsObjectsD_ctl[0].value(0) #Off display tens-zero
        else:
            pinsObjectsD_ctl[0].value(1)
        # Mostrar decenas
        for i in range(len(pinsObjectsD)):
            machine.Pin(displayTensPins[i], machine.Pin.OUT).value((digit_map[tens] >> i) & 1)
        #time.sleep(0.005)  # Tiempo para visualizar
        # Mostrar unidades
        for i in range(len(pinsObjectsU)):
            machine.Pin(displayUnitsPins[i], machine.Pin.OUT).value((digit_map[ones] >> i) & 1)
        #time.sleep(1)  # Tiempo para visualizar

# def countDown(seconds):
#     global running
#     running = True
#     while seconds >= 0 and running:
#         displayNumber(displayUnidades_pins, seconds)
#         #display_number(display2_pins, seconds)
#         time.sleep(1)
#         seconds -= 1
#     running = False

#countdown(countdown_value)
#######################################################################################
#SATATE MACHINE
#######################################################################################
#--------------------------------------------------------------------------------------
class StateMachine:
    def __init__(self):
        self.state = 'START'  # START
        self.countDown = countdownValue
        self.button = 0
        self.doorSen= 0
        self.startT = time.ticks_ms() # get millisecond counter, opcional

    def run(self):
        # Map states to functions (methods)
        estados = {
            'START':    self.state0,
            'SETTINGENV': self.state1,
            'WAITING':  self.state2,
            'PLAYING':  self.state3,
        }
        while True:
            estados[self.state]()  # Llama a la función del estado actual

    def state0(self):   #-------------------------------------------START
        print("START")
        #GENERAL SETTINGS
        setupDisplayU(displayUnidadesPins)  #Make espesific pins outputs
        setupDisplayD(displayDecenasPins)
        self.turbine=setupOutput(pinTurbine)
        self.extractor=setupOutput(pinExtractor)
        self.ligth=setupOutput(pinLigth)

        self.button=setupInput(pinButton) #Make button_pin input
        self.doorSen=setupInput(pinDoorSen)

        time.sleep_ms(sleep_time)
    
        self.state = 'SETTINGENV'

    def state1(self):   #-------------------------------------------READY2GO
        print("SETTINGENV")
    
        displayNumber(displayDecenasPins, displayUnidadesPins,self.countDown)
        self.turbine.value(0)
        self.extractor.value(0)
        self.ligth.value(1)
        
        self.state = 'WAITING'  # Cambia al siguiente estado

    def state2(self):   #-------------------------------------------PLAYING
        print("WAITING...")
        #print("Button: " + str(self.button.value()))
        #print("Door Sensor: " + str(self.doorSen.value()))

        if( (self.button.value() == 0) and (self.doorSen.value()==1) ):
            self.state = 'PLAYING'
            print("PLAYING")
            self.turbine.value(1)
            self.extractor.value(1)
            self.startT = time.ticks_ms() # get millisecond counter

    def state3(self):   #-------------------------------------------ERROR
        
        if( (time.ticks_diff(time.ticks_ms(), self.startT)) >= 1000 ):
            displayNumber(displayDecenasPins, displayUnidadesPins, self.countDown)
            self.startT = time.ticks_ms() # get millisecond counter
            self.countDown=self.countDown-1

        if( self.doorSen.value() == 0 or self.countDown < 0):
            time.sleep_ms(1)
            self.state = 'SETTINGENV'
            self.countDown = countdownValue
        

        
maquina = StateMachine() 
maquina.run()             

# from machine import Pin

for i in range(0, 40):
    try:
        p = Pin(i, Pin.OUT)
        print(f'Pin {i} configurado correctamente.')
    except ValueError:
        print(f'Pin {i} no es válido.')

for i in range(0, len(displayUnidades_pins)):
    print(P_objects[i].value())