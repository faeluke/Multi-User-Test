import sys
from pyvisa import ResourceManager


class AG34401:
    def __init__(self, address: str):
        """
        :param address: GPIB address of multimeter.
        """
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        identity = self.__inst.query("*IDN?").split(',')
        if identity[1][:5] != '34401':
            print('Device at {} is not a Agilent 34401.'.format(address))
            sys.exit()

    def measure_dc_voltage(self):
        """
        :return: Return the float of DC voltage measurement.
        """
        return float(self.__inst.query('measure:voltage:dc?'))

    def measure_dc_current(self):
        """
        :return: Return the float of DC current measurement.
        """
        return float(self.__inst.query('measure:current:dc?'))

    def measure_ac_voltage(self):
        """
        :return: Return the float of AC voltage measurement.
        """
        return float(self.__inst.query('measure:voltage:ac'))

    def measure_ac_current(self):
        """
        :return: Return the float of AC current measurement.
        """
        return float(self.__inst.query('measure:current:ac'))

    def close(self):
        self.__inst.close()


