from PySide6.QtGui import QFont, QIcon, QGuiApplication
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QApplication, QPushButton
from PySide6.QtCore import Qt, QPoint
# from pyqt_svg_button import SvgButton


class NotifierWidget(QWidget):
    def __init__(self, informative_text='', detailed_text=''):
        super().__init__()
        self.__initUi(informative_text, detailed_text)

    def __initUi(self, informative_text='', detailed_text=''):
        self.setFixedSize(250, 150)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)

        self.__informativeTextLabel = QLabel(informative_text) if informative_text else QLabel('Informative')
        self.__informativeTextLabel.setFont(QFont('Arial', 15, QFont.Weight.Bold))
        self.__detailedTextLabel = QLabel(detailed_text) if detailed_text else QLabel('Detailed')

        closeBtn = QPushButton()
        closeBtn.clicked.connect(self.close)
        closeBtn.setIcon(QIcon('pyqt_notifier/ico/close.svg'))

        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        self.__btnWidget = QWidget()
        self.__btnWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        lay.addWidget(closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        customMenuBar = QWidget()
        customMenuBar.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(customMenuBar)
        lay.addWidget(self.__informativeTextLabel)
        lay.addWidget(self.__detailedTextLabel)
        lay.addWidget(self.__btnWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        ag = QGuiApplication.primaryScreen().availableGeometry()

        geo = self.geometry()
        geo.moveBottomRight(QPoint(ag.width(), ag.height()))
        self.setGeometry(geo)

        lay.setContentsMargins(8, 8, 8, 8)
        self.setLayout(lay)
        self.setStyleSheet('QWidget { background: #222; color: #DDD; }')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.close()

        return super().keyPressEvent(e)

    def addWidgets(self, widgets: list):
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
            self.__btnWidget.layout().addWidget(widget)

    def show(self) -> None:
        super().show()
        QApplication.beep()
