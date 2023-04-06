import sys

from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from src.bot import start_tg


import json
import shutil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/static/design/main.ui', self)

        self.progressbar = ProgressBarThread()
        self.progressbar.message_update.connect(self.connect_service, QtCore.Qt.QueuedConnection)
        self.progressbar.start()

        # # кнопки для открытия других форм
        # self.btn_file.clicked.connect(self.path_account)
        # self.btn_steam.clicked.connect(self.path_steam)
        # self.btn_cs.clicked.connect(self.path_cs)
        # self.btn_start.clicked.connect(self.start_farm)
        # self.btn_start_server.clicked.connect(start_server)
        # self.btn_setup.clicked.connect(self.mem)
        # self.btn_sandboxie.clicked.connect(self.path_sandboxie)
        # self.btn_start_steam.clicked.connect(self.start_steams)
        #
        # # создание настроек юзера
        # self.settings = {}
        # self.load_settings_user()
        # print('Настройки юзера', *self.settings.items())
        #
        # # Выводим данные на экран
        # self.txt_steam.setText(self.settings['path_steam'])
        # self.txt_cs.setText(self.settings['path_cs'])
        # self.txt_file.setText(self.settings['path_accounts'])
        # self.txt_sandboxie.setText(self.settings['path_sandboxie'])
        # self.edit_server.setText(self.settings['server'])
        # self.edit_interval_start.setText(self.settings['interval_start'])
        # self.edit_user_account_id.setText(self.settings['account_id'])
        #
        # self.progressbar = ProgressBarThread()

    # Коннект между тг и интерфейсом
    def connect_service(self, s):
        print(s)
        self.test_text.setText(s)


def show_inreface():
    print('Показываем интерфейс')

    app = QApplication(sys.argv)

    screen = MainWindow()
    screen.show()
    screen.setWindowTitle('CodeRun')
    # screen.setWindowIcon(QtGui.QIcon('./settings/icon_test.ico'))
    sys.exit(app.exec_())


class ProgressBarThread(QThread):
    # сигналы
    message_update = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    # определяем откуда сигнал
    def run(self):
        print('1123')
        start_tg(self)


if __name__ == '__main__':
    show_inreface()
