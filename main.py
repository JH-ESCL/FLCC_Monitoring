import i2c_ina219 as ina, i2c_ltc4151 as ltc, max7318atg_code as max, define as d, server as sv
import threading as th
import sys

def init():
    max.write_data(0x58, 0x02, 0xf8)
    max.write_data(0x58, 0x06, 0xf8)
    
def main_def():
    ina.read_i2c()
    ltc.ltc4151()
    max.getmax()
    
    th.Timer(0.1, main_def).start()

if __name__ == "__main__":
    init()
    main_def()
    
    print("read start... waiting..")
    
    th.Thread(target=sv.createServer).start()
    
    
    