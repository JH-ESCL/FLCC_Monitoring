import socket
import sys
import threading
import define as d, max7318atg_code as m, crc16

s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_ptr = 0
recv = []

def readyRead(addr):
    try:
        while True:
            data = c_sock.recv(4096)
            collect_data(data.decode())
    except Exception as e:
        print(f"Exception: {e}")
    except KeyboardInterrupt:
        print("stop")
        
def collect_data(data):
    global _ptr
    for i in range(0 ,len(data)):
        if(_ptr > 256):
            _ptr = 0
            recv.clear()
        
        if(data[i] == '$' and _ptr == 0):
            recv.append(data[i])
            _ptr += 1
        elif(data[i] == '\n'):
            recv.append(data[i])
            analyze_data(recv)
            _ptr = 0
            recv.clear()
        else:
            recv.append(data[i])    
            _ptr += 1
            
def analyze_data(data):
    cdata = (''.join(data[0:9])).encode()
    crc_room = (''.join(data[9:13]))
    crc = crc16.crc16(cdata, 0, len(cdata))
    if(f'{crc:x}' == crc_room.lower()):
        if(data[0] == "$" and data[1] == "C" and data[2] == "T" and data[3] == "L"):
            if(data[5] == "0"):
                m.write_data(0x58, 0x02, data[7])
        
def sendData():
    try:
        a = d.get_ina()
        b = d.get_ltc()
        c = d.get_max()
        
        packet = f"$STS,{a.volt0},{a.curr0},{a.volt1},{a.curr1},{a.volt2},{a.curr2},{a.volt3},{a.curr3},{a.volt4},{a.curr4},{a.volt5},{a.curr5},{a.volt6},{a.curr6},{a.volt7},{a.curr7},{a.volt8},{a.curr8},{a.volt9},{a.curr9},{a.volt10},{a.curr10},{a.volt11},{a.curr11},{b.mpv1},{b.mpc1},{b.mpv2},{b.mpc2},{b.smv1},{b.smc1},{b.smv2},{b.smc2},{b.smv3},{b.smc3},{b.smv4},{b.smc4},{c.mux0},{c.mux1},{c.mux2},{c.mpmf1},{c.mpmv1},{c.mpmc1},{c.mpmf2},{c.mpmv2},{c.mpmc2},{c.mpsf1},{c.mpsv1},{c.mpsc1},{c.mpsf2},{c.mpsv2},{c.mpsc2}*"
        # print(packet)
        crc = crc16.crc16(packet.encode(), 0, len(packet.encode()))
        packet = packet + f'{crc:x}' + "\r\n"
        c_sock.sendall(packet.encode())
        
        threading.Timer(0.1, sendData).start()
        
    except Exception as e:
        print(f"Exception: {e}")
        
def sendErrData(erraddr):
    try:
        packet = f"$ERR,{erraddr}*"
        crc = crc16.crc16(packet.encode(), 0, len(packet.encode()))
        packet = packet + f'{crc:x}' + "\r\n"
        c_sock.sendall(packet.encode())
        
    except Exception as e:
        print(f"Exception: {e}")

def createServer():
    print("waiting connection...")
    threading.Thread(target=input_thread, args=(m,), daemon=True).start()
    try: 
        s_sock.bind(('', 4321))
        s_sock.listen(10)
        while True:
            try:
                global c_sock
                c_sock, addr = s_sock.accept()
                print(f"{addr} is connected")
                newConnection = threading.Thread(target=readyRead, args=[addr])
                newConnection.start()
                sendata = threading.Timer(0.1, sendData)
                sendata.start()
            except Exception as e:
                print(f"An error occurred while accepting a connection: {e}")
    except Exception as e:
        print(f"An error occurred while setting up the server: {e}")

        


# JH 20240307 MUX selection
def input_thread(m):
    global mux_chan
    while True:
        try:
            new_chan = int(input("MUX Channel Number : "))
            if new_chan > 3 or new_chan <= 0:
                print("Wrong Channel Number!")
            else:
                mux_chan = new_chan
                print(f"MUX channel {mux_chan} is selected!")
                if mux_chan == 1:
                    m.write_data(0x58, 0x02, 1)
                if mux_chan == 2:
                    m.write_data(0x58, 0x02, 2)
                if mux_chan == 3:
                    m.write_data(0x58, 0x02, 4)
        except ValueError:
            print("Please enter a valid integer.")
        except Exception as e:
            print(f"An error occurred in the input thread: {e}")

