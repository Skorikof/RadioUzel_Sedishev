import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, Qt
from MainUi import Ui_MainWindow
from SensUi import Ui_SensWindow
from Settings import SettingsPrg
from Threads import ReaderBase
import LogPrg


class WindowReadBaseSignal(QObject):
    startRead = pyqtSignal()
    stopRead = pyqtSignal()
    exitRead = pyqtSignal()


class ChangeUi(QMainWindow):
    def __init__(self):
        super(ChangeUi, self).__init__()
        self.main_win = Ui_MainWindow()
        self.main_win.setupUi(self)
        self.logger = LogPrg.get_logger(__name__)
        self.set_prg = SettingsPrg()
        self.threadpool = QThreadPool()
        self.signals = WindowReadBaseSignal()

        self.change_ui()

        self.initThreadReadBase()

    def change_ui(self):
        try:
            self.scan_action = QAction('Сканировать', self)
            self.main_win.menubar.addAction(self.scan_action)
            self.scan_action.triggered.connect(self.scanBase)

        except Exception as e:
            self.logger.error(e)

    def scanBase(self):
        try:
            if not self.set_prg.isRunReadBase:
                if self.set_prg.initPort:
                    self.set_prg.isRunReadBase = True
                    self.scan_action.setText('Прекратить сканирование')
                    self.startReadBase()

            else:
                self.set_prg.isRunReadBase = False
                self.scan_action.setText('Сканировать')
                self.set_prg.client.close()
                self.stopReadBase()

        except Exception as e:
            self.logger.error(e)

    def initThreadReadBase(self):
        try:
            read_base = ReaderBase(self.set_prg.client, 1, self.set_prg.timeout_betsend)
            read_base.signals.result_base.connect(self.resultReadBase)
            read_base.signals.error.connect(self.errorReadBase)
            read_base.signals.error_read.connect(self.errorReadBase)
            read_base.signals.error_modbus.connect(self.errorModBus)
            self.signals.startRead.connect(read_base.startThread)
            self.signals.stopRead.connect(read_base.stopThread)
            self.signals.exitRead.connect(read_base.exitThread)

            self.threadpool.start(read_base)

        except Exception as e:
            self.logger.error(e)

    def startReadBase(self):
        self.signals.startRead.emit()

    def stopReadBase(self):
        self.signals.stopRead.emit()

    def exitReadBase(self):
        self.signals.exitRead.emit()

    def resultReadBase(self, data):
        try:
            print(data)

        except Exception as e:
            self.logger.error(e)

    def errorReadBase(self, data):
        try:
            print(data)

        except Exception as e:
            self.logger.error(e)

    def errorModBus(self, data):
        try:
            print(data)

        except Exception as e:
            self.logger.error(e)

    def showMsg(self, type_m, text_title, text_info, flag_exit):
        try:
            msg = QMessageBox()
            if type_m == 'error':
                a = QMessageBox.Critical
            if type_m == 'info':
                a = QMessageBox.Information
            if type_m == 'warning':
                a = QMessageBox.Warning
            msg.setIcon(a)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(text_title)
            msg.setInformativeText(text_info)
            msg.setWindowFlag(Qt.WindowStaysOnTopHint)
            retval = msg.exec_()
            if flag_exit:
                sys.exit(0)

        except Exception as e:
            self.logger.error(str(e))