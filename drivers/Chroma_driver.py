import sys
from pyvisa import ResourceManager

'''
Created on Janurar 10, 2025

@author: brownlaw
'''

class C6310A(object):
    """ Version 0.0.0.1 Static only
    This Embodies the static load functionality. """
    def __init__(self, address: str):
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        identity = self.__inst.query("*IDN?").split(',')
        if "C631" not in identity[1]:
            print('Device at {} is not an Chroma 6310.'.format(address))
            sys.exit()

    def Set_Channel(self, channel):
        if channel in ('1','2','3','4','5','6','7','8','MIN','MAX'): 
            if channel == '1':
                Outval = "CHAN 1"
            elif channel =='2' :
                Outval = "CHAN 2"
            elif channel =='3' :
                Outval = "CHAN 3"
            elif channel =='4' :
                Outval = "CHAN 4"
            elif channel =='5' :
                Outval = "CHAN 5"
            elif channel =='6' :
                Outval = "CHAN 6"
            elif channel =='7' :
                Outval = "CHAN 7"
            elif channel =='8' :
                Outval = "CHAN 8"
#            print "Set_Channel", Outval
            self.__inst.write(Outval)
        else :
            print("Unrecognized Command -> Set_Channel <-")
            
    def Get_Channel(self):
        return int(self.dev.ask("CHAN?"))
    #output = property(Get_Channel, Set_Channel, None, "Current Active Channel")

class C63200:
    def __init__(self, address: str):
        """
        :param address: GPIB address
        """
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        identity = self.__inst.query("*IDN?").split(',')
        if "632" not in identity[1]:
            print(identity[1])
            print('Device at {} is not a Chroma Load.'.format(address))
            sys.exit()
    
   
    def Set_Channel_Active(self, state):
        if state in ('0','1','ON','OFF'): 
            if state == '0' or state == 'OFF' :
                Outval = "CHAN:ACT 0"
            else :
                Outval = "CHAN:ACT 1"
#                print "Set_Channel_Active", Outval
                
            self.__inst.write(Outval)
        else :
            print("Unrecognized Command -> Set_Channel_Active <-")
    
    def Set_Load_Active(self):
        Outval = "LOAD 1"
        self.__inst.write(Outval)

    def Set_Load_Inactive(self):
        Outval = "LOAD 0"
        self.__inst.write(Outval)

    def Set_Mode(self, mode):
        if mode in ('CCL','CCH','CCDL','CCDH','CRL', 'CRH', 'CV'): 
            Outval = "MODE "+ mode           
            self.__inst.write(Outval)
        else :
            print("Unrecognized Command -> Set_Mode <-")          

    def Set_Static_Current_L1(self, value):
        Outval = "CURR:STAT:L1 {}" .format(value)
        self.__inst.write(Outval)
            
    def Set_Static_Current_L2(self, value):
        Outval = "CURR:STAT:L2 {}" .format(value)
        self.__inst.write(Outval)
            
    def Set_Static_Rise(self, val):
        Outval = "CURR:STAT:RISE {}".format(val)    
        self.__inst.write(Outval)
            
    def Set_Static_Fall(self, val):
        Outval = "CURR:STAT:FALL {}".format(val)    
        self.__inst.write(Outval)
            
    def Set_Static_Rise_MAX(self):
        Outval = "CURR:STAT:RISE MAX"      
        self.__inst.write(Outval)
            
    def Set_Static_Fall_MAX(self):
        Outval = "CURR:STAT:FALL MAX"     
        self.__inst.write(Outval)
            

    def _Measure_Voltage(self):
        return self.__inst.query("MEAS:VOLT?")
    
    def _Measure_Current(self):
        return self.__inst.query("MEAS:CURR?")
    
    def Measure_Voltage(self, chnl):
        self.Set_Channel(chnl)
        return self.__inst.query("MEAS:VOLT?")
    
    def Measure_Current(self, chnl):
        self.Set_Channel(chnl)
        return self.__inst.query("MEAS:CURR?")
    
    
       
