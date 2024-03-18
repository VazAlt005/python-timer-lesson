import sys

from PySide6.QtWidgets import QWidget, QPushButton, QDialog, QSizePolicy, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QTime, QSettings, Qt
from PySide6.QtGui import QIcon

from pyqt_notifier.pyqtNotifier import NotifierWidget
from pyqt_timer.settingsDialog.settingsDialog import SettingsDialog
from pyqt_timer_label.timerLabel import TimerLabel
# from pyqt_svg_button import SvgButton


class Timer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__settings_struct = QSettings('timerSettings.ini', QSettings.Format.IniFormat)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self._hour = int(self.__settings_struct.value('hour', 0))  # type: ignore
        self._min = int(self.__settings_struct.value('min', 0))  # type: ignore
        self._sec = int(self.__settings_struct.value('sec', 0))  # type: ignore

        self._startPauseBtn = QPushButton(self)
        self._refreshBtn = QPushButton(self)
        self._stopBtn = QPushButton(self)
        self._settingsBtn = QPushButton(self)

        self._btnWidget = QWidget()
        self._timerLbl = TimerLabel(self)

    def __initUi(self):
        self._startPauseBtn.setToolTip('Start')
        self._refreshBtn.setToolTip('Refresh')
        self._stopBtn.setToolTip('Stop')
        self._settingsBtn.setToolTip('Settings')

        btns = [self._startPauseBtn, self._refreshBtn, self._stopBtn, self._settingsBtn]

        self._startPauseBtn.setIcon(QIcon('pyqt_timer/ico/play.svg'))
        self._refreshBtn.setIcon(QIcon('pyqt_timer/ico/refresh.svg'))
        self._stopBtn.setIcon(QIcon('pyqt_timer/ico/stop.svg'))
        self._settingsBtn.setIcon(QIcon('pyqt_timer/ico/settings.svg'))

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for btn in btns:
            btn.setMaximumWidth(btn.sizeHint().width())
            lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        self._btnWidget.setLayout(lay)

        self._timerLbl.doubleClicked.connect(self.__settings)
        self._timerLbl.resetSignal.connect(self.__reset)
        self._timerLbl.stopped.connect(self.__stop)
        self._timerLbl.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(self._timerLbl)
        lay.addWidget(self._btnWidget)
        lay.setAlignment(self._btnWidget, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(lay)

        self.__timerInit()

        # for preventing the "hard to make window smaller" problem
        self.setMinimumSize(self.sizeHint())

    def __setStartHMS(self):
        self._timerLbl.setStartHour(self._hour)
        self._timerLbl.setStartMinute(self._min)
        self._timerLbl.setStartSecond(self._sec)

    def __timerInit(self):
        self._startPauseBtn.setObjectName('start')

        self._startPauseBtn.clicked.connect(self.__start)
        self._refreshBtn.clicked.connect(self.__refresh)
        self._stopBtn.clicked.connect(self._timerLbl.reset)
        self._settingsBtn.clicked.connect(self.__settings)

        self.__setStartHMS()

        self._startPauseBtn.setEnabled(self._timerLbl.text() != '00:00:00')
        self._refreshBtn.setEnabled(False)
        self._stopBtn.setEnabled(False)

    def __start(self):
        try:
            if self._startPauseBtn.objectName() == 'start':
                self.__prepare()
                self._timerLbl.start()
                self._startPauseBtn.setObjectName('pause')
                self._startPauseBtn.setIcon(QIcon('pyqt_timer/ico/pause.svg'))
                self._startPauseBtn.clicked.connect(self.__pauseOrRestart)
                self._refreshBtn.setEnabled(True)
                self._stopBtn.setEnabled(True)
        except Exception as e:
            print(e)
            info = sys.exc_info()
            assert info[2]
            print(info[2].tb_lineno)
            print(info)

    def __prepare(self):
        self._settingsBtn.setEnabled(False)
        self._timerLbl.doubleClicked.disconnect(self.__settings)

    def __pauseOrRestart(self):
        try:
            if self._startPauseBtn.objectName() == 'pause':
                self._timerLbl.pause()
                self._startPauseBtn.setIcon(QIcon('pyqt_timer/ico/play.svg'))
                self._startPauseBtn.setToolTip('Restart')
                self._startPauseBtn.setObjectName('restart')
            elif self._startPauseBtn.objectName() == 'restart':
                self._timerLbl.restart()
                self._startPauseBtn.setIcon(QIcon('pyqt_timer/ico/pause.svg'))
                self._startPauseBtn.setToolTip('Pause')
                self._startPauseBtn.setObjectName('pause')
        except Exception as e:
            print(e)

    def __notifyTimesUp(self):
        self.__notifier = NotifierWidget('Notice', 'Times up.')
        notifierRefreshBtn = QPushButton('Restart')
        notifierRefreshBtn.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        notifierRefreshBtn.clicked.connect(self.__start)
        self.__notifier.addWidgets([notifierRefreshBtn])
        self.__notifier.show()

    def __refresh(self):
        if self._timerLbl.isPaused():
            self._timerLbl.refresh()
        else:
            self._timerLbl.reset()

    def __reset(self):
        self._startPauseBtn.setToolTip('Start')
        self._startPauseBtn.setObjectName('start')
        self._startPauseBtn.setIcon(QIcon('pyqt_timer/ico/play.svg'))

        self._startPauseBtn.clicked.disconnect(self.__pauseOrRestart)
        self._startPauseBtn.clicked.connect(self.__start)

        self._settingsBtn.setEnabled(True)
        self._refreshBtn.setEnabled(False)
        self._stopBtn.setEnabled(False)

        self._timerLbl.doubleClicked.connect(self.__settings)

    def __stop(self):
        try:
            self.__reset()
            self.__notifyTimesUp()
        except Exception as e:
            print(e)
            info = sys.exc_info()
            assert info[2]
            print(info[2].tb_lineno)
            print(info)

    def __settings(self):
        dialog = SettingsDialog()
        reply = dialog.exec()
        if reply == QDialog.DialogCode.Accepted:
            self._hour, self._min, self._sec = dialog.get_time()

            # self.__show_event_f = dialog.get_show_event_list_flag()
            self.__taskTimeLeft = QTime(self._hour, self._min, self._sec)
            task_time_text = self.__taskTimeLeft.toString('hh:mm:ss')

            self._timerLbl.setText(task_time_text)
            self._startPauseBtn.setEnabled(task_time_text != '00:00:00')

            self.__setStartHMS()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Space:
            self.__pauseOrRestart()
        return super().keyPressEvent(e)
