import socket
import sys
import threading
import define as d, max7318atg_code as m, crc16
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import csv
csv_filename = './log/data_log.csv'

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
        
        # Define your headers (labels) based on your packet data structure
        headers = ['time', 'a.volt0', 'a.curr0', 'a.volt1', 'a.curr1', 'a.volt2', 'a.curr2', 'a.volt3', 'a.curr3', 'a.volt4', 'a.curr4', 'a.volt5', 'a.curr5', 'a.volt6', 'a.curr6', 'a.volt7', 'a.curr7', 'a.volt8', 'a.curr8', 'a.volt9', 'a.curr9', 'a.volt10', 'a.curr10', 'a.volt11', 'a.curr11', 'b.mpv1', 'b.mpc1', 'b.mpv2', 'b.mpc2', 'b.smv1', 'b.smc1', 'b.smv2', 'b.smc2', 'b.smv3', 'b.smc3', 'b.smv4', 'b.smc4', 'c.mux0', 'c.mux1', 'c.mux2', 'c.mpmf1', 'c.mpmv1', 'c.mpmc1', 'c.mpmf2', 'c.mpmv2', 'c.mpmc2', 'c.mpsf1', 'c.mpsv1', 'c.mpsc1', 'c.mpsf2', 'c.mpsv2', 'c.mpsc2']

        # Check if the file exists and has content
        file_exists = os.path.isfile(csv_filename) and os.path.getsize(csv_filename) > 0

        with open(csv_filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the headers if the file is new or empty
            if not file_exists:
                csvwriter.writerow(headers)
            # Then write the data row
            csvwriter.writerow(packet.split(','))

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
                threading.Thread(target=plot_log, args=(), daemon=True).start()
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

def plot_log():
    plt.ion()  # Enable interactive mode
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 18))  # Create three subplots

    while True:
        try :             
            sendata = threading.Timer(0.1, sendData)
            sendata.start()

            # Load the data from the CSV file
            data = pd.read_csv(csv_filename)

            # Clear existing data in plots
            ax1.clear()
            ax2.clear()
            ax3.clear()

            # Plot 'a' series data: assuming it's voltage and current data
            for i in range(12):  # 12 pairs of voltage and current
                ax1.plot(data[f'a.volt{i}'], label=f'Voltage {i} (V)')
                ax1.plot(data[f'a.curr{i}'], label=f'Current {i} (A)', linestyle='--')

            # Plot 'b' series data: adapt the number based on your specific data
            ax2.plot(data['b.mpv1'], label='b.mpv1 (V)')
            ax2.plot(data['b.mpc1'], label='b.mpc1 (A)')
            ax2.plot(data['b.mpv2'], label='b.mpv2 (V)')
            ax2.plot(data['b.mpc2'], label='b.mpc2 (A)')
            # Add more plots for the 'b' series if needed

            # Plot 'c' series data: adapt this part to your specific 'c' series data structure
            ax3.plot(data['c.mux0'], label='c.mux0')
            ax3.plot(data['c.mux1'], label='c.mux1')
            ax3.plot(data['c.mux2'], label='c.mux2')
            ax3.plot(data['c.mpmf1'], label='c.mpmf1')
            # Add more plots for the 'c' series if needed

            # Adding legends and setting labels
            ax1.legend(loc='upper left')
            ax1.set_title('Series a Data')
            ax1.set_xlabel('Sample')
            ax1.set_ylabel('Value')

            ax2.legend(loc='upper left')
            ax2.set_title('Series b Data')
            ax2.set_xlabel('Sample')
            ax2.set_ylabel('Value')

            ax3.legend(loc='upper left')
            ax3.set_title('Series c Data')
            ax3.set_xlabel('Sample')
            ax3.set_ylabel('Value')

            # Use plt.pause to allow interactive updating. This can be adjusted or removed depending on your use case
            plt.pause(0.1)

        except Exception as e:
            print(f"An error occurred in the plot and log: {e}")
        time.sleep(1)  # Update interval; adjust as needed for your use case
