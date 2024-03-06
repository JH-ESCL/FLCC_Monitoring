import collections
_ina = collections.namedtuple('ina', 'volt0 curr0 volt1 curr1 volt2 curr2 volt3 curr3 volt4 curr4 volt5 curr5 volt6 curr6 volt7 curr7 volt8 curr8 volt9 curr9 volt10 curr10 volt11 curr11')
_ltc = collections.namedtuple('ltc' , 'mpv1 mpc1 mpv2 mpc2 smv1 smc1 smv2 smc2 smv3 smc3 smv4 smc4')
_max = collections.namedtuple('max', 'mux0 mux1 mux2 mpmf1 mpmv1 mpmc1 mpmf2 mpmv2 mpmc2 mpsf1 mpsv1 mpsc1 mpsf2 mpsv2 mpsc2 can1 can2 canas1 canas2 canaf1 canaf2 canaf3 canbs1 canbs2 canbf1 canbf2 canbf3')

def get_ina():
    return ina
    
def set_ina(data):
    global ina
    ina = _ina(volt0=data[0], curr0=data[1],
               volt1=data[2], curr1=data[3],
               volt2=data[4], curr2=data[5],
               volt3=data[6], curr3=data[7],
               volt4=data[8], curr4=data[9],
               volt5=data[10], curr5=data[11],
               volt6=data[12], curr6=data[13],
               volt7=data[14], curr7=data[15],
               volt8=data[16], curr8=data[17],
               volt9=data[18], curr9=data[19],
               volt10=data[20], curr10=data[21],
               volt11=data[22], curr11=data[23])
    
def get_ltc():
    return ltc

def set_ltc(data):
    global ltc
    ltc = _ltc(mpv1=data[0], mpc1=data[1],
               mpv2=data[2], mpc2=data[3],
               smv1=data[4], smc1=data[5],
               smv2=data[6], smc2=data[7],
               smv3=data[8], smc3=data[9],
               smv4=data[10], smc4=data[11])
    
def get_max():
    return max7318

def set_max(data):
    global max7318
    max7318 = _max(mux0=data[0][0], mux1=data[0][1], mux2=data[0][2], 
                   mpmf1=data[0][3], mpmv1=data[0][4], mpmc1=data[0][5],
                   mpmf2=data[0][6], mpmv2=data[0][7], mpmc2=data[1][0], 
                   mpsf1=data[1][1], mpsv1=data[1][2], mpsc1=data[1][3],
                   mpsf2=data[1][4], mpsv2=data[1][5], mpsc2=data[1][6], 
                   can1=data[2][0], can2=data[2][1], 
                   canas1=data[2][2], canas2=data[2][3], 
                   canaf1=data[2][4], canaf2=data[2][5], canaf3=data[2][6],
                   canbs1=data[2][7], canbs2=data[3][0], 
                   canbf1=data[3][1], canbf2=data[3][2], canbf3=data[3][4])\

