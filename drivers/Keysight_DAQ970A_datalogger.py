#----------------------------------------------------------------
#Device Model: Keysight DAQ970A
#Version: V1
#Last Modified Date: 2026 March 10
#----------------------------------------------------------------

import pyvisa as visa
import time

class DAQ970A():
    
#    def __init__(self, desc):
#        rm = visa.ResourceManager()
#        self.visa = rm.open_resource(desc)
#        ident = self.get_ident()
#        if not ('DAQ970A' in ident):
#            print("Warning, attached device", desc, "is not a Keysight DAQ970A DAQ")
#            print("Device is", ident)
#        return
    
    def get_ident(self):
        'Return the identity of the device'
        return self.visa.query('*IDN?')
    
    def clear_errors(self):
        self.visa.write('*CLS')
    
    def release(self, safe=True):
        try:
            if safe:
                self.visa.write('LOAD OFF')
                self.visa.write('*CLS')
                self.visa.write('SYST:LOC')
        except Exception:
            pass
        finally:
            try:
                self.visa.clear()
            except Exception:
                pass
            self.visa.close()        

    def arm(self):
        'changes the state of the triggering system from idle to wait-for-trigger'
        self.visa.write('INIT')

    def trigger(self):
        'Triggers the instrument when bus trigger is selected'
        self.visa.write('*TRG')
    
    def DC_meas(self, range, res, channel): #page 106
        self.visa.write('CONF:VOLT:DC {},{},(@{})'.format(str(range), str(res), str(channel)))        
 
    def set_scan_list(self, channel):
        self.visa.write('ROUT:SCAN (@{})'.format(str(channel)))
    
    def set_bus_trigger(self, count): 
        self.visa.write('TRIG:SOUR BUS') #Sets the trigger source for measurements, BUS = Software tirgger
        self.visa.write(f'TRIG:COUN {int(count)}')
        #self.visa.write('INIT')
        
    def fetch(self, channels = 1):
        'Fetch the measurement after a bus trigger'
        return list(map(float, self.visa.query('FETC?').strip().split(',')))
    
    def abort(self):
        self.visa.write('ABOR')
    
    def temp_meas(self, tc, channel):
        #tc = thermocouple type e.g. K, T, J, etc.
        temp = self.visa.query('MEAS:TEMP? TC,{},(@{})'.format(str(tc), str(channel)))
        return float(temp)

    def set_trigger_count(self, count):
        self.visa.write('TRIG:COUNT ' + str(count))
        
    def get_unit(self):
        return self.visa.query('FORM:READ:UNIT?')
    
    def read_error(self):
        return self.visa.query('SYSTEM:ERROR?')