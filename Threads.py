import time
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from pymodbus.exceptions import ModbusException as ModEx


class ReadBaseSignals(QObject):
    result_base = pyqtSignal(object)
    error = pyqtSignal(object)
    error_read = pyqtSignal(object)
    error_modbus = pyqtSignal(object)


class ReaderBase(QRunnable):
    signals = ReadBaseSignals()

    def __init__(self, client, dev_id, timeout_bs):
        super(ReaderBase, self).__init__()
        self.cycle = True
        self.is_run = False
        self.client = client
        self.dev_id = dev_id
        self.timeout_betSend = timeout_bs
        self.num_attempt = 0
        self.max_attempt = 3

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    while self.num_attempt < self.max_attempt:
                        rr = self.client.read_holding_registers(0, 14, unit=1)
                        if not rr.isError():
                            # self.num_attempt = self.max_attempt
                            self.signals.result_base.emit(rr)
                            time.sleep(0.5)

                        else:
                            self.num_attempt += 1
                            if self.num_attempt == self.max_attempt:
                                self.signals.error_read.emit(rr)
                            if not self.timeout_betSend == 0:
                                time.sleep(self.timeout_betSend)

            except ModEx as e:
                self.signals.error_modbus.emit(e)
                time.sleep(1)

            except Exception as e:
                self.signals.error.emit(str(e))

    def startThread(self):
        self.is_run = True

    def stopThread(self):
        self.is_run = False

    def exitThread(self):
        self.cycle = False
