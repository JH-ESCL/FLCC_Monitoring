import smbus
import define as d

i2c = smbus.SMBus(5)

def read_data(chip, addr):
    try:
        return i2c.read_byte_data(chip, addr)
    except Exception as ex:
        print("max read data error")

def write_data(chip, addr, data):
    try:
        i2c.write_byte_data(chip, addr, data)
    except Exception as ex:
        print("max write data error")
    
def analyze(anal):
    try:
        max = [0,0,0,0,0,0,0,0]
        max[0] = 1 if anal & 0x01 == 0x01 else 0
        max[1] = 1 if anal & 0x02 == 0x02 else 0
        max[2] = 1 if anal & 0x04 == 0x04 else 0
        max[3] = 1 if anal & 0x08 == 0x08 else 0
        max[4] = 1 if anal & 0x10 == 0x10 else 0
        max[5] = 1 if anal & 0x20 == 0x20 else 0
        max[6] = 1 if anal & 0x40 == 0x40 else 0
        max[7] = 1 if anal & 0x80 == 0x80 else 0
        
        return max
    except Exception as ex:
        print("max analyze error")
    
def getmax():
    a0 = read_data(0x58, 0x00)
    a1 = read_data(0x58, 0x01)
    a2 = read_data(0x5f, 0x00)
    a3 = read_data(0x5f, 0x01)
    
    max0 = analyze(a0)
    max1 = analyze(a1)
    max2 = analyze(a2)
    max3 = analyze(a3)
    
    max_data = [max0 , max1, max2, max3]
    d.set_max(max_data)
    
