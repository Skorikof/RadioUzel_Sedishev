import serial
import configparser
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class SettingsPrg(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('Settings.ini')

        self.portNumber = 'COM' + config.get('ComPort', 'NumberPort')
        temp = config.get('ComPort', 'PortSettings').split(',')
        self.baudrate = int(temp[0])
        self.parity = temp[1]
        self.databits = int(temp[2])
        self.stopbits = int(temp[3])
        self.available_ports = self.scan_ports()

        self.repeater_mode = False
        temp = config.get('PrgSet', 'RepeaterMod')
        if temp.upper() == 'TRUE':
            self.repeater_mode = True

        temp = config.get('PrgSet', 'Timeout(ms)')
        self.timeout_send = int(temp)

        temp = config.get('PrgSet', 'TimeBetweenSend(ms)')
        self.timeout_betsend = int(temp)

        self.isRunReadBase = False

        a = self.initPort(self.timeout_send)

    def scan_ports(self):
        available = []
        for i in range(256):
            try:
                s = serial.Serial('COM' + str(i))
                available.append(s.portstr)
                s.close()

            except serial.SerialException:
                pass
        return available

    def initPort(self, timeout_s):
        self.client = ModbusClient(method='rtu', port=self.portNumber, timeout=timeout_s / 1000,
                                   baudrate=self.baudrate, stopbits=self.stopbits, databits=self.databits,
                                   parity=self.parity, strict=False)

        port_connect = self.client.connect()

        if port_connect:
            return True
        else:
            return False
