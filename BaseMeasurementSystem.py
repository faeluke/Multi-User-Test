import abc
from typing import Dict

class Base_Source(abc.ABC):

    @abc.abstractmethod
    def set_voltage(self,voltage:float):pass

    @abc.abstractmethod
    def enable_output(self,state:bool):pass


class BaseLoad(abc.ABC):

    @abc.abstractmethod
    def set_ccurrent(self,current:float):pass

    
class BaseMeasurementSystem(abc.ABC):
    """
    Abstract interface for acquiring power path measurements.
    Hides whether data comes from 4 independent DMMs or 1 multi-channel DAQ.
    """
    
    @abc.abstractmethod
    def read_power_data(self) -> Dict[str, float]:
        """
        Reads instrument channels and returns a unified dictionary.
        Expected keys: 'vin', 'iin', 'vout', 'iout'
        """
        pass