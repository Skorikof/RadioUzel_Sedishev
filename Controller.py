import sys
from PyQt5.QtWidgets import QApplication
from View import ChangeUi


class Application(ChangeUi):
    def __init__(self):
        super(Application, self).__init__()

    def closeEvent(self, event):
        try:
            self.signals.exitRead.emit()
            self.set_prg.client.close()

        except Exception as e:
            self.logger.error(e)


def main():
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
