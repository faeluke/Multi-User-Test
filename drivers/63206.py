#----------------------------------------------------------------
#Device Model: Chroma63206A-1200-240
#Version: V1
#Last Modified Date: 2026 March 9
#----------------------------------------------------------------

import pyvisa as visa
import time

class Chroma_63206A():
    def __init__(self, desc):

        rm = visa.ResourceManager()
        self.visa = rm.open_resource(desc)

        ident = self.get_ident()
        if not ('63206A' in ident):
            print("Warning, attached device", desc, "is not a Chroma 63206A load")
            print("Device is", ident)
        return
    
    def get_ident(self):
        return self.visa.query('*IDN?')
    
    def clear_errors(self):
        self.visa.write('*CLS')

    def set_state(self, state):
        'Turn on/off the load'
        self.visa.write('LOAD '+str(state))

    def short(self, state):
        'Activate/Inactivate short-circuited simulation'
        self.visa.write('LOAD:SHOR '+str(state))

    def get_function(self):
        return self.visa.query('MODE?')

    def set_function(self, mode):
        'mode: CCL, CCM, CCH, CRL, CRM, CRH, CVL, CVM, CVH, CPL, CPM, CPH, CCDL, CCDH, CRDL, CRDH, CCEL, CCEH'
        self.visa.write('MODE ' + str(mode))

    def meas_power(self):
        return self.visa.query('FETC:POW?')

    def meas_curr(self):
        return self.visa.query('FETC:CURR?')

    def meas_voltage(self):
        return float(self.visa.query('FETC:VOLT?'))
    
    def release(self, safe=True):
        try:
            if safe:
                self.visa.write('LOAD OFF')
                self.visa.write('*CLS')
                time.sleep(0.5)
                self.visa.write('SYST:LOC')
        except Exception:
            pass
        finally:
            try:
                self.visa.clear()
            except Exception:
                pass
            self.visa.close()

#Constant Voltage Mode

    def set_voltage(self, L, value):
        'set the static load voltage in constant voltage mode'
        self.visa.write('VOLT:STAT:{} {}'.format(L, value))
        
    def set_current_max(self, value):
        'set the current limit for constant voltage mode'
        self.visa.write('VOLT:STAT:ILIM {}'.format(str(value)))

#Constant Current Mode

    def set_cc_curr(self, L, value):
        'Set the static load current for constant current static mode'
        self.visa.write('CURR:STAT:{} {}'.format(L, value))

    def get_cc_curr(self, L):
        'Return static constant current value of specified channel'
        return self.visa.query('CURR:STAT:{}?'.format(L))
    
    def get_all_curr(self):
        'Return static constant current values of all channels'
        L1 = float(self.visa.query('CURR:STAT:L1?'))
        L2 = float(self.visa.query('CURR:STAT:L2?'))
        return L1, L2

# Slew rate control

    def get_slew_rate(self, mode, slope):
        'Return the rising/falling slew rate of current in A/us for specified mode'
        return self.visa.query('{}:STAT:{}?'.format(mode, slope))

    def set_slew_rate(self, mode, slope, value):
        'Set the rising/falling slew rate of current in A/us for specified mode'
        'mode: CURR, VOLT, RES, POW'
        'slope: RISE, FALL'
        self.visa.write('{}:STAT:{} {}'.format(mode, slope, value))

# Constant Resistance Mode

    def set_cr_res(self, L, value):
        'Set the static resistance level for constant resistance mode'
        self.visa.write('RES:STAT:{} {}'.format(L, value))

    def get_cr_res(self, L):
        'Return the static resistance level of specified channel'
        return self.visa.query('RES:STAT:{}?'.format(L))
    
    def get_all_res(self):
        'Return the static resistance level of all channels'
        L1 = float(self.visa.query('RES:STAT:L1?'))
        L2 = float(self.visa.query('RES:STAT:L2?'))
        return L1, L2

# Constant Power Mode

    def set_cp_pow(self, L, value):
        'Set the static power for constant power mode'
        self.visa.write('POW:STAT:{} {}'.format(L, value))

    def get_cp_pow(self, L):
        'Return the static power of specified channel'
        return self.visa.query('POW:STAT:{}?'.format(L))

    def get_all_pow(self):
        'Return the static power of all channels'
        L1 = float(self.visa.query('POW:STAT:L1?'))
        L2 = float(self.visa.query('POW:STAT:L2?'))
        return L1, L2



# Dynamic Mode Operation

    def get_dyn_curr(self, L):
        'Return constant current dynamic setting of specified channel'
        return self.visa.query('CURR:DYN:{}?'.format(L))

    def set_dyn_curr(self, L, curr):
        'set the high and low currents for constant current dynamic mode'
        self.visa.write('CURR:DYN:{} {} '.format(L, curr))

    def get_dyn_res(self, L):
        'Return constant resistance dynamic setting of specified channel'
        return self.visa.query('RES:DYN:{}?'.format(L))

    def set_dyn_res(self, L, res):
        'set the high and low resistnaces for constant resistance dynamic mode'
        self.visa.write('RES:DYN:{} {} '.format(L, res))

    def set_dyn(self, mode, func, value):
        'mode: CURR, RES'
        'func: L1/L2, T1/T2, REP, RISE, FALL, VRNG'
        'value units: Amp, second, A/us'
        self.visa.write('{}:DYN:{} {}'.format(mode, func, value))