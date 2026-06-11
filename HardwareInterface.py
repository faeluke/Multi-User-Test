
from abc import ABC, abstractmethod

class BaseEfficiencyTester(ABC):
    """Abstract interface that any hardware setup must implement."""
    
    @abstractmethod
    def configure_input_voltage(self, voltage: float):
        pass

    @abstractmethod
    def set_load(self, current: float):
        pass

    @abstractmethod
    def measure_metrics(self) -> dict:
        """Must return a dict with keys: 'v_in', 'i_in', 'v_out', 'i_out'"""
        pass