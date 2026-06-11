#----------------------------------------------------------------
#Device Model: B&K Precision MR50040
#Version: V1
#Last Modified Date: 2026 March 9
#----------------------------------------------------------------

import pyvisa as visa
from drivers.base import basePS
class BK_MR50040(basePS):
    
#    def __init__(self, desc):
#        rm = visa.ResourceManager()
#        self.visa = rm.open_resource(desc)
#        ident = self.get_ident()
#        if not ('MR50040' in ident):
#            print("Warning, attached device", desc, "is not a MR50040")
#            print("Device is", ident)
#        return
    
    def get_ident(self):
        'Return the identity of the device'
        return self.visa.query('*IDN?')
    
    def release(self, safe=True):
        try:
            if safe:
                self.visa.write('OUTP OFF')
                self.visa.write('*CLS')
            self.visa.write('SYST:COMM:RLST LOC')
        except Exception:
            pass
        finally:
            try:
                self.visa.clear()
            except Exception:
                pass
            self.visa.close()
    
    def get_errors (self):
        self.visa.write('SYST:ERR?')
                        
    def clear_errors(self):
        'clear faults'
        self.visa.write('*CLS')

    def set_state(self, state):
        self.visa.write('OUTP '+str(state))

    def set_voltage(self, volt):
        'set output voltage'
        self.visa.write('VOLT '+str(volt))
    
    def set_voltage_slewrate(self, slew):
        'set voltage rising slew rate in V/ms'
        self.visa.write('VOLT:SLEW '+str(slew))

    def set_max_voltage(self, vmax):
        'configures the maximum voltage limit'
        self.visa.write('VOLT:MAX '+str(vmax))
    
    def set_current(self,curr):
        self.visa.write('SOUR:CURR '+str(curr))

    def set_current_slewrate(self, currslew):
        'set current rising slew rate in mA/ms'
        self.visa.write('CURR:SLEW '+str(currslew))
    
    def set_max_current(self,cmax):
        'configures the maximum current limit'
        self.visa.write('CURR:MAX '+str(cmax))


    