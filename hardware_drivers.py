import pyvisa
from hardware_interface import BaseEfficiencyTester

class ShuntSetupTester(BaseEfficiencyTester):
    """YOUR SETUP: Measures current via voltage drop across a shunt resistor."""
    def __init__(self):
        # rm = pyvisa.ResourceManager()
        # self.dmm = rm.open_resource('GPIB0::22::INSTR')
        self.shunt_resistance = 0.010  # 10 mOhms
        
    def configure_input_voltage(self, voltage):
        pass # Code to set source voltage
        
    def set_load(self, current):
        pass # Code to set electronic load
        
    def measure_metrics(self):
        # Example: Measure voltage drop across output shunt
        v_shunt = 0.050 # self.dmm.query_ascii_values('MEAS:VOLT:DC?')[0]
        i_out = v_shunt / self.shunt_resistance
        
        return {
            "v_in": 12.0,
            "i_in": i_out * 1.15, # Example input scaling
            "v_out": 5.0,
            "i_out": i_out
        }

class DirectSupplyTester(BaseEfficiencyTester):
    """COLLEAGUE'S SETUP: Queries the power supply directly via SCPI."""
    def __init__(self):
        # rm = pyvisa.ResourceManager()
        # self.supply = rm.open_resource('TCPIP0::192.168.1.100::INSTR')
        pass
        
    def configure_input_voltage(self, voltage):
        pass
        
    def set_load(self, current):
        pass
        
    def measure_metrics(self):
        # Queries built-in readback commands directly from instruments
        # i_out = float(self.supply.query("MEASure:CURRent?"))
        return {
            "v_in": 12.0,
            "i_in": 2.2,
            "v_out": 5.0,
            "i_out": 2.0
        }