from ina219 import INA219
from ina219 import DeviceRangeError
import define as d

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

def read_i2c():
    try:
        ina0 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x40)
        ina0.configure(ina0.RANGE_16V, ina0.GAIN_1_40MV)

        ina1 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x41)
        ina1.configure(ina1.RANGE_16V, ina1.GAIN_1_40MV)

        ina2 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x42)
        ina2.configure(ina2.RANGE_16V, ina2.GAIN_1_40MV)

        ina3 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x43)
        ina3.configure(ina3.RANGE_16V, ina3.GAIN_1_40MV)

        ina4 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x44)
        ina4.configure(ina4.RANGE_16V, ina4.GAIN_1_40MV)

        ina5 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x45)
        ina5.configure(ina5.RANGE_16V, ina5.GAIN_1_40MV)

        ina6 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x46)
        ina6.configure(ina6.RANGE_16V, ina6.GAIN_1_40MV)

        ina7 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x47)
        ina7.configure(ina7.RANGE_16V, ina7.GAIN_1_40MV)

        ina8 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x48)
        ina8.configure(ina8.RANGE_16V, ina8.GAIN_1_40MV)

        ina9 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x49)
        ina9.configure(ina9.RANGE_16V, ina9.GAIN_1_40MV)

        ina10 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x4a)
        ina10.configure(ina10.RANGE_16V, ina10.GAIN_1_40MV)

        ina11 = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x4b)
        ina11.configure(ina11.RANGE_16V, ina11.GAIN_1_40MV)
        
        ina_data=[round(ina0.voltage(),3), round(ina0.current(),3), round(ina1.voltage(),3), round(ina1.current(),3), round(ina2.voltage(),3), round(ina2.current(),3), round(ina3.voltage(),3), round(ina3.current(),3), round(ina4.voltage(),3), round(ina4.current(),3), round(ina5.voltage(),3), round(ina5.current(),3), round(ina6.voltage(),3), round(ina6.current(),3), 
                  round(ina7.voltage(),3), round(ina7.current(),3), round(ina8.voltage(),3), round(ina8.current(),3), round(ina9.voltage(),3), round(ina9.current(),3), round(ina10.voltage(),3), round(ina10.current(),3), round(ina11.voltage(),3), round(ina11.current(),3)]

        d.set_ina(ina_data)
        
        # print(f'3. V1 : {ina0.voltage()} V , {ina0.current()} A / V2 : {ina1.voltage()} V , {ina1.current()} A')
        # print(f'4. V1 : {ina2.voltage()} V , {ina2.current()} A / V2 : {ina3.voltage()} V , {ina3.current()} A')
        # print(f'5. V1 : {ina4.voltage()} V , {ina4.current()} A / V2 : {ina5.voltage()} V , {ina5.current()} A')
        # print(f'6. A : {ina6.voltage()} V , {ina6.current()} A / B : {ina7.voltage()} V , {ina7.current()} A / C : {ina8.voltage()} V , {ina8.current()} A')
        # print(f'7. V1 : {ina9.voltage()} V , {ina9.current()} A / V2 : {ina10.voltage()} V , {ina10.current()} A')
        # print(f'8. V1 : {ina11.voltage()} V , {ina11.current()} A')
    except DeviceRangeError as ex:
        print("에러뜸")

