import socket
import sys
import threading
import define as d, max7318atg_code as m, crc16

s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_ptr = 0
recv = []

def readyRead(c_sock, addr):
    try:
        while True:
            data = c_sock.recv(4096)
            collect_data(data.decode())
    except Exception as e:
        print(f"Exception: {e}")
    except KeyboardInterrupt:
        print("정지됨")
        
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
                print("here")
                m.write_data(0x58, 0x02, data[7])
        
def sendData(c_sock):
    try:
        a = d.get_ina()
        b = d.get_ltc()
        c = d.get_max()
        
        packet = f"$STS,{a.volt0},{a.curr0},{a.volt1},{a.curr1},{a.volt2},{a.curr2},{a.volt3},{a.curr3},{a.volt4},{a.curr4},{a.volt5},{a.curr5},{a.volt6},{a.curr6},{a.volt7},{a.curr7},{a.volt8},{a.curr8},{a.volt9},{a.curr9},{a.volt10},{a.curr10},{a.volt11},{a.curr11},{b.mpv1},{b.mpc1},{b.mpv2},{b.mpc2},{b.smv1},{b.smc1},{b.smv2},{b.smc2},{b.smv3},{b.smc3},{b.smv4},{b.smc4},{c.mux0},{c.mux1},{c.mux2},{c.mpmf1},{c.mpmv1},{c.mpmc1},{c.mpmf2},{c.mpmv2},{c.mpmc2},{c.mpsf1},{c.mpsv1},{c.mpsc1},{c.mpsf2},{c.mpsv2},{c.mpsc2},{c.can1},{c.can2},{c.canas1},{c.canas2},{c.canaf1},{c.canaf2},{c.canaf3},{c.canbs1},{c.canbs2},{c.canbf1},{c.canbf2},{c.canbf3}*"
        # print(packet)
        crc = crc16.crc16(packet.encode(), 0, len(packet.encode()))
        packet = packet + f'{crc:x}' + "\r\n"
        
        c_sock.sendall(packet.encode())
        
        threading.Timer(0.1, sendData, args=[c_sock]).start()
    except Exception as e:
        print(f"Exception: {e}")

def createServer():
    print("waiting connection...")
    
    s_sock.bind(('', 4321))
    s_sock.listen(10)
    while True:
        c_sock, addr = s_sock.accept()
        print(f"{addr} is connected")
        newConnection = threading.Thread(target=readyRead, args=[c_sock, addr])
        newConnection.start()
        sd = threading.Timer(0.1, sendData, args=[c_sock])
        sd.start()
        
def input_thread(m):
    global mux_chan
    while True:
        try:
            new_chan = int(input("MUX Channel Number : "))
            if new_chan > 3 or new_chan < 0:
                print("Wrong Channel Number!")
            else:
                mux_chan = new_chan
                print(f"MUX channel {mux_chan} is selected!")
                m.write_data(0x58, 0x02, mux_chan)
        except ValueError:
            print("Please enter a valid integer.")