from abc import ABC, abstractmethod

class BasePowerSupply(ABC):
    """Abstract Interface that all PSU drivers must implement."""
    
    def __init__(self, visa_resource, config: dict):
        self.instr = visa_resource
        self.config = config
        self.max_voltage = config.get("max_voltage", 0.0)
        
    @abstractmethod
    def set_voltage(self, volts: float):
        pass

    @abstractmethod
    def enable_output(self, state: bool):
        pass

    #@abstractmethod
    #def measure_power(self) -> float:
    #   pass

