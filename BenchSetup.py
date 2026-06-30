
import importlib
from MeasurementOptions import DaqMeasurementSystem, QuadDmmMeasurementSystem


# --- BEGIN SIMULATED HARDWARE BACKENDS (Replace with actual PyVISA classes) ---
class MockSource:
    def __init__(self, resource_id, **kwargs): self.res = resource_id
    def set_voltage(self, voltage: float): pass
    def enable_output(self, state: bool): pass

class MockLoad:
    def __init__(self, resource_id, **kwargs): self.res = resource_id
    def set_current(self, current: float): pass

class MockDmm:
    def __init__(self, resource_id, **kwargs): self.res = resource_id
    def read_voltage(self) -> float: return 4.95  # Simulated raw reading voltage drop

class MockDaq:
    def __init__(self, resource_id, **kwargs): self.res = resource_id
    def scan_channels(self, channels: list) -> dict:
        return {ch: 4.95 for ch in channels} # Simulated multi-channel response
# --- END SIMULATED HARDWARE BACKENDS ---

class IntrumentFactory:
    """
    Dynamically imports and creates any single hardware driver instance.
    Uniformly maps Source, Load, DAQ, or DMM from the identical YAML format.

    Args:
        config (dict): _description_

    Raises:
        ImportError: _description_
        AttributeError: _description_

    Returns:
    """
    @staticmethod
    def create_instrument(config: dict):


        driver_path =config["Module_Name"]
        class_name = config["Device"]
        resource_id = config["Addr"]
        #safeties = config.get("safeties",{}) # not implemented
        
                            
        try:
            module = importlib.import_module(driver_path)

            driver_class = getattr(module,class_name)

        except ModuleNotFoundError:
            raise ImportError(f"Could not find driver file: '{driver_path}.py'")
        except AttributeError:
            raise AttributeError(f"Class '{class_name}' not found inside '{driver_path}.py'")

        print (resource_id,"resource id")

        return driver_class(resource_id)

    
    @classmethod
    def build_measurement_engine(cls, strategy: str, inst_configs: dict, setup_configs: dict):
        """
                Assembles the abstract measurement driver system layer.

        Args:
            strategy (str): _description_
            inst_configs (dict): _description_
            setup_configs (dict): _description_

        Returns:
            _type_: _description_

        Yields:
            _type_: _description_
        """


        strategy_params = setup_configs.get(strategy, {})
        mapping = strategy_params["mapping"]
        shunts = strategy_params["shunts"]

        if strategy == "daq":
            # Extract configuration and spin up the DAQ driver
            daq_hardware = cls.create_instrument(inst_configs["daq_device"])
            return DaqMeasurementSystem(
                daq_device=daq_hardware, 
                mapping=mapping, 
                shunts=shunts
            )
            
        elif strategy == "quad_dmm":
            # Spin up 4 independent DMM drivers using identical format handling
            return QuadDmmMeasurementSystem(
                dmm_vin=cls.create_instrument(inst_configs[mapping["vin"]]),
                dmm_iin=cls.create_instrument(inst_configs[mapping["iin"]]),
                dmm_vout=cls.create_instrument(inst_configs[mapping["vout"]]),
                dmm_iout=cls.create_instrument(inst_configs[mapping["iout"]]),
                shunts=shunts
            )
            
        else:
            raise ValueError(f"Unknown measurement strategy: {strategy}")



