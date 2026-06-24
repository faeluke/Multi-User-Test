from BaseMeasurementSystem import BaseMeasurementSystem

from typing import Dict

class QuadDmmMeasurementSystem(BaseMeasurementSystem):
    def __init__(self, dmm_vin, dmm_iin, dmm_vout, dmm_iout,shunts: Dict):
        self.dmm_vin = dmm_vin
        self.dmm_iin = dmm_iin
        self.dmm_vout = dmm_vout
        self.dmm_iout = dmm_iout
        self.r_iin = shunts.get("iin_ohms", 1.0)
        self.r_iout = shunts.get("iout_ohms", 1.0)


    def read_power_data(self) -> Dict[str, float]:
        # Triggers sequential or concurrent readings across 4 standalone meters
        v_in = self.dmm_vin.read_voltage()
        v_iin_shunt = self.dmm_iin.read_voltage()
        v_out = self.dmm_vout.read_voltage()
        v_iout_shunt = self.dmm_iout.read_voltage()
        
        return {
            "vin": float(v_in),
            "iin": float(v_iin_shunt / self.r_iin),   # I = V / R
            "vout": float(v_out),
            "iout": float(v_iout_shunt / self.r_iout)  # I = V / R
        }
    
class DaqMeasurementSystem(BaseMeasurementSystem):
    def __init__(self, daq_device, mapping:Dict, shunts:Dict):
        self.daq = daq_device
        self.map = mapping
        self.r_iin = shunts.get("iin_ohms",1.0)
        self.r_iout = shunts.get("iout_ohms",1.0)

    def read_power_data(self) -> Dict[str, float]:
        # Typically DAQs scan multiple channels in a single optimized block/burst read

        channels = [self.map["vin"],self.map["iin"],self.map["vout"],self.map["iout"]]
        raw_scan = self.daq.scan_channels(channels) # Returns list/dict of raw floats

        v_iin_shunt= raw_scan[self.map["iin"]]
        v_iout_shunt= raw_scan[self.map["iout"]]
        
        return {
            "vin": float(raw_scan[self.map["vin"]]),
            "iin": float(v_iin_shunt/self.r_iin),
            "vout": float(raw_scan[self.map["vout"]]),
            "iout": float(v_iout_shunt/self.r_iout)
        }

class InstrumentBench:
    """The master container wrapping all live hardware on the selected bench."""
    def __init__(self, input_source, driver_source, system_load, aux_source, measurement_system: BaseMeasurementSystem):
        self.input_source = input_source
        self.driver_source = driver_source
        self.system_load = system_load
        self.meters = measurement_system
        self.ctrl_source = aux_source

    def emergency_shutdown(self):
        """Safe teardown execution loop."""
        try:
            self.system_load.set_current(0.0)
            self.input_source.enable_output(False)
            self.driver_source.enable_output(False)
        except Exception as e:
            print(f"\nCRITICAL: Teardown routine failed to trip safe states! {e}")
 