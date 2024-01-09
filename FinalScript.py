import threading  # Import to libery
import pyads  # Import van libery
import telnetlib  # Import van libery
import time  # Import van libery

# Making a connection with the PLC
AMSNETID = "10.100.1.10.1.1"  # IP address of PLC (IP address for demo)
plc = pyads.Connection(AMSNETID, 851)  # Port of PLC
plc.open()
print(f"Connected?: {plc.is_open}")  # Making sure the PLC is connected
print(f"Local Address?: {plc.get_local_address()}")  # Printed with what address
print(f"symbols?: {plc.get_all_symbols()}")  # Making sure all the symbols are usable
PLC_commandos = ''

HOST = '10.38.4.171'  # IP address of the AMR
PORT = 7171  # Port of the AMR

state = 0  # Begin case of the process
AMR_EStop = False  # Begin state of variable
AMR_Ready = False  # Begin state of variable
AMR_RUN = True  # Begin state of variable

telnet_lock = threading.Lock()  # Setting up communication with AMR and PLC
string_received_event = threading.Event()  # Same as above


def MainScript():  # Script of the whole process
    with telnetlib.Telnet(HOST, PORT) as tn:  # Making connection with the AMR 'Tara'
        tn.read_until(b'Enter password:\r\n')  # System asking for password
        tn.write(b'adept\r\n')  # Giving password 'adept'
        tn.read_until(b'End of commands\r\n')
        while AMR_RUN:
            global state
            symbol_EmergencyStop = plc.get_symbol('IO.EmergencyStop')  # Asking for 'TRUE' or 'FALSE' of the button
            Emergency = symbol_EmergencyStop.read()
            if not Emergency:  # When button is FALSE
                tn.write(b'Stop\r\n')
                print("Emergency has been pressed")
                state = 'Emergency'
            if AMR_EStop:  # When ESTOP on AMR is pressed
                print("AMR EStop has been pressed")
                state = 'AMR EStop'
            match state:
                case 0:
                    symbol_StartButton = plc.get_symbol('IO.StartButton')  # Asking for 'TRUE' or 'FALSE'
                    Start = symbol_StartButton.read()
                    symbol_PLC_Ready = plc.get_symbol('IO.PLC_Ready')  # Asking for 'TRUE' or 'FALSE'
                    PLC_Ready = symbol_PLC_Ready.read()
                    if Start and PLC_Ready and Emergency and not AMR_EStop:
                        print("Going to begin position")
                        state = 1
                    symbol_TrayRequest = plc.get_symbol('IO.TrayRequest')  # Asking for 'TRUE' or 'FALSE'
                    Request = symbol_TrayRequest.read()
                    if Request and Emergency and not AMR_EStop and AMR_Ready:
                        print("Tray has been requested")
                        state = 2
                case 1:
                    tn.write(b'GoTo Beginpositie_AMR\r\n')  # Going to begin position
                    state = 0
                case 2:
                    tn.write(b'patrolonce DemoRoute\r\n')  # Patrolling the Route of demo
                    state = 0
                case 'Emergency':
                    symbol_EmergencyStop = plc.get_symbol('IO.EmergencyStop')  # Asking for 'TRUE' or 'FALSE'
                    Emergency = symbol_EmergencyStop.read()
                    symbol_ResetButton = plc.get_symbol('IO.ResetButton')  # Asking for 'TRUE' or 'FALSE'
                    Reset = symbol_ResetButton.read()
                    tn.write(b'outputOff o1\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o2\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o3\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o4\r\n')  # disable output on AMR, AMR doesnt do it itself
                    if Reset and Emergency and not AMR_EStop:
                        print("Has been reset")
                        tn.write(b'patrolonce BlokkersBeneden\r\n')
                        tn.read_until(b'Finished patrolling route BlokkersBeneden\r\n')
                        tn.write(b'GoTo Beginpositie_AMR\r\n')  # Going to begin position
                        state = 0
                case 'AMR EStop':
                    tn.write(b'outputOff o1\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o2\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o3\r\n')  # disable output on AMR, AMR doesnt do it itself
                    time.sleep(0.1)
                    tn.write(b'outputOff o4\r\n')  # disable output on AMR, AMR doesnt do it itself
                    if tn.read_until(b'Motors enabled'):  # Asking for 'TRUE' or 'FALSE'
                        tn.write(b'patrolonce BlokkersBeneden\r\n')
                        tn.read_until(b'Finished patrolling route BlokkersBeneden\r\n')
                        tn.write(b'GoTo Beginpositie_AMR\r\n')  # Going to begin position
                        state = 0


def Script2():  # AMR EStop
    with telnetlib.Telnet(HOST, PORT) as tn:  # Making connection with the AMR 'Tara'
        tn.read_until(b'Enter password:\r\n')  # System asking for password
        tn.write(b'adept\r\n')  # Giving password 'adept'
        tn.read_until(b'End of commands\r\n')
        while AMR_RUN:
            global AMR_EStop
            if tn.read_until(b'EStop pressed'):   # Asking for 'TRUE' or 'FALSE'
                AMR_EStop = True
                if tn.read_until(b'Motors enabled'):  # Asking for 'TRUE' or 'FALSE'
                    AMR_EStop = False


def Script3():  # AMR Position Ready
    with telnet_lock:
        with telnetlib.Telnet(HOST, PORT) as tn:  # Making connection with the AMR 'Tara'
            tn.read_until(b'Enter password:\r\n')  # System asking for password
            tn.write(b'adept\r\n')  # Giving password 'adept'
            tn.read_until(b'End of commands\r\n')
            while AMR_RUN:
                global AMR_Ready
                AMR_Ready = False
                response = tn.read_until(b'Waiting for string\r\n', timeout=0.5).decode('utf-8')
                if "Finished patrolling route DemoRoute" in response:  # Finished the demo route
                    while AMR_RUN:
                        AMR_Ready = True
                        symbol_TrayRequest = plc.get_symbol('IO.TrayRequest')  # Asking for 'TRUE' or 'FALSE'
                        Request = symbol_TrayRequest.read()
                        if Request:
                            time.sleep(1)
                            break
                elif "Arrived at Beginpositie_AMR" in response:  # Arrived at begin position
                    while AMR_RUN:
                        AMR_Ready = True
                        symbol_TrayRequest = plc.get_symbol('IO.TrayRequest')  # Asking for 'TRUE' or 'FALSE'
                        Request = symbol_TrayRequest.read()
                        if Request:
                            time.sleep(1)
                            break


#  Making all scripts process together at the same time
while AMR_RUN:
    thread_AMR_EStop = threading.Thread(target=Script2)
    thread_MainScript = threading.Thread(target=MainScript)
    thread_AMR_Ready = threading.Thread(target=Script3)
    thread_MainScript.start()
    thread_AMR_EStop.start()
    thread_AMR_Ready.start()
    thread_MainScript.join()
    thread_AMR_EStop.join()
    thread_AMR_Ready.join()
