import sys
from pyvisa import ResourceManager


class HP6032:
    def __init__(self, address: str):
        """
        :param address: GPIB address
        """
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        #identity = self.__inst.query("*IDN?").split(',')
        #if "6402A" not in identity[1]:
        #    print('Device at {} is not a Agilent E364x.'.format(address))
        #    sys.exit()

    def set_voltage_and_current(self, voltage: float, current: float):
        """
        :param voltage: Desired output voltage
        :param current: Desired output current
        """

        self.__inst.write("VSET {}".format(voltage))
        self.__inst.write("ISET {}".format(current))


    def enable_output(self):
        self.__inst.write("OUTP ON")

    def disable_output(self):
        self.__inst.write("OUTP OFF")

    def close(self):
        self.__inst.close()
