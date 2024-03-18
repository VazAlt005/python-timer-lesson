from PySide6.QtWidgets import QApplication
from pyqt_timer.timer import Timer
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    timerGadget = Timer()
    timerGadget.show()
    sys.exit(app.exec())