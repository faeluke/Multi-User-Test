import sys
from pyvisa import ResourceManager


class N8934:
    def __init__(self, address: str):
        """
        :param address: GPIB address
        """
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        identity = self.__inst.query("*IDN?").split(',')
        if "N8934" not in identity[1]:
            print (identity[1],identity[2])
            print('Device at {} is not an Agilent N8934.'.format(address))
            sys.exit()

    def set_voltage(self, voltage: float, current: float):
        """
        :param voltage: Desired output voltage
        :param current: Desired output current
        """
        self.__inst.write("VOLT {}" .format(voltage))
        self.__inst.write("CURR {}" .format(current))
                          
                          

    def enable_output(self):
        self.__inst.write("OUTP ON")

    def disable_output(self):
        self.__inst.write("OUTP OFF")

    def close(self):
        self.__inst.close()

class E3631:
    def __init__(self, address: str):
        """
        :param address: GPIB address of multimeter.
        """
        self.__rm = ResourceManager()
        self.__inst = self.__rm.open_resource(address)
        identity = self.__inst.query("*IDN?").split(',')
        if identity[1][:5] != 'E3631':
            print('Device at {} is not a Agilent E3631.'.format(address))
            sys.exit()

    def Select_6V(self):
        """
        :return: Return the float of DC voltage measurement.
        """
        self.__inst.write('INST:SEL P6V')
    def Select_25V(self):
        """
        :return: Return the float of DC voltage measurement.
        """
        self.__inst.write('INST:SEL P25V')

    def set_voltage1(self, voltage: float, current: float):
        """
        :param voltage: Desired output voltage
        :param current: Desired output current
        """
        self.__inst.write('INST:SEL P6V')
        self.__inst.write("VOLT {}" .format(voltage))
        self.__inst.write("CURR {}" .format(current))
                          
                          
    def set_voltage2(self, voltage: float, current: float):
        """
        :param voltage: Desired output voltage
        :param current: Desired output current
        """
        self.__inst.write('INST:SEL P25V')
        self.__inst.write("VOLT {}" .format(voltage))
        self.__inst.write("CURR {}" .format(current))
                          
                          

    def enable_output(self):
        self.__inst.write("OUTP ON")

    def disable_output(self):
        self.__inst.write("OUTP OFF")

    def close(self):
        self.__inst.close()



    def measure_voltage1(self):
        """
        :return: Return the float of DC voltage measurement.
        """
        self.__inst.write('INST:SEL P6V')
        return float(self.__inst.query('meas? p6v'))

    def measure_voltage2(self):
        """
        :return: Return the float of DC voltage measurement.
        """
        self.__inst.write('INST:SEL P25V')
        return float(self.__inst.query('meas? p25v'))

    def measure_current1(self):
        """
        :return: Return the float of DC current measurement.
        """
        self.__inst.write('INST:SEL P6V')
        return float(self.__inst.query('meas:curr? P6V'))

    def measure_current2(self):
        """
        :return: Return the float of DC current measurement.
        """
        self.__inst.write('INST:SEL P25V')
        return float(self.__inst.query('meas:curr? P25V'))

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
