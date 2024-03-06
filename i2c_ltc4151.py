import smbus
import define as d

i2c = smbus.SMBus(1)

def ltc4151():
    try:
        main_power1_volt = i2c.read_i2c_block_data(0x67, 0x02, 2)
        main_power1_curr = i2c.read_i2c_block_data(0x67, 0x00, 2)
        main_power2_volt = i2c.read_i2c_block_data(0x68, 0x02, 2)
        main_power2_curr = i2c.read_i2c_block_data(0x68, 0x00, 2)

        servo_mot_1_volt = i2c.read_i2c_block_data(0x69, 0x02, 2)
        servo_mot_1_curr = i2c.read_i2c_block_data(0x69, 0x00, 2)
        servo_mot_2_volt = i2c.read_i2c_block_data(0x6a, 0x02, 2)
        servo_mot_2_curr = i2c.read_i2c_block_data(0x6a, 0x00, 2)
        servo_mot_3_volt = i2c.read_i2c_block_data(0x6b, 0x02, 2)
        servo_mot_3_curr = i2c.read_i2c_block_data(0x6b, 0x00, 2)
        servo_mot_4_volt = i2c.read_i2c_block_data(0x6c, 0x02, 2)
        servo_mot_4_curr = i2c.read_i2c_block_data(0x6c, 0x00, 2)
        
        ltc_data = [calc_volt(main_power1_volt), calc_curr(main_power1_curr), 
                    calc_volt(main_power2_volt), calc_curr(main_power2_curr),
                    calc_volt(servo_mot_1_volt), calc_curr(servo_mot_1_curr),
                    calc_volt(servo_mot_2_volt), calc_curr(servo_mot_2_curr),
                    calc_volt(servo_mot_3_volt), calc_curr(servo_mot_3_curr),
                    calc_volt(servo_mot_4_volt), calc_curr(servo_mot_4_curr)]
        
        d.set_ltc(ltc_data)

        # print(f'1. V1 : {calc_volt(main_power1_volt)} VDC, {calc_curr(main_power1_curr)} A /'
        #     f' V2 : {calc_volt(main_power2_volt)} VDC, {calc_curr(main_power2_curr)} A')
        # print(f'2. V1 : {calc_volt(servo_mot_1_volt)} VDC, {calc_curr(servo_mot_1_curr)} A /'
        #     f'V2 : {calc_volt(servo_mot_2_volt)} VDC, {calc_curr(servo_mot_2_curr)} A /'
        #     f'V3 : {calc_volt(servo_mot_3_volt)} VDC, {calc_curr(servo_mot_3_curr)} A /'
        #     f'V4 : {calc_volt(servo_mot_4_volt)} VDC, {calc_curr(servo_mot_4_curr)} A /')
    except Exception as ex:
        print("ltc4151 error")


def calc_volt(value):
    try:
        value = int.from_bytes(value, byteorder='big')
        return round((value >> 4) * 102.4 / 4096.0, 3)
    except Exception as ex:
        print("ltc calc volt error")


def calc_curr(value):
    try:
        value = int.from_bytes(value, byteorder='big')
        return round((value >> 4) * 81.92 / 4096.0 / 0.1, 3)
    except Exception as ex:
        print("ltc calc curr error")
