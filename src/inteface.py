import sys

from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QStringListModel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel

from src.bot import start_tg
from src.game import Game

import json
import shutil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/static/design/main.ui', self)

        self.game = Game()
        self.game.create_code_game()

        # slm = QStringListModel()
        # slm.setStringList(['1', '2', '3'])
        # self.listView.setModel(slm)

        self.progressbar = ProgressBarThread(self.game, self)
        self.progressbar.message_update.connect(self.connect_service, QtCore.Qt.QueuedConnection)
        self.progressbar.start()

        self.init_ui()

    def init_ui(self):

        self.code_game_text.setText(self.game.code_game)

        # self.table_view.setColumnCount(3)  # Set three columns
        # self.table_view.setRowCount(1)  # and one row
        #
        # self.table_view.setItem(1, 1, 1)
        pixmap = QPixmap('src/static/img/1 Tiles/Map_tile_17.png')

        # for i in range(1, 101):
        #     label = self.findChild(QLabel, f'label_{i}')
        #     label.setPixmap(pixmap)

            # self.setCentralWidget(label)
            # self.resize(pixmap.width(), pixmap.height())
        # self.paint()

        self.player.setPixmap(QPixmap('src/static/img/player one.png').scaled(40, 40))
        self.player.move(5, -40)
        self.player.hide()

        # # кнопки для открытия других форм
        # self.btn_file.clicked.connect(self.path_account)
        # self.btn_steam.clicked.connect(self.path_steam)

    def player_shows(self, data):
        from time import sleep

        x, y = 40, 40
        move_player = {
            'вверх': [(-y, 0), (-1, 0)],
            'вниз': [(y, 0), (1, 0)],
            'влево': [(-x, 0), (-1, 0)],
            'вправо': [(x, 0), (1, 0)]
        }

        pobeda = []

        for user, code in data.items():
            x_s, x_e = -10, 20
            print(user)
            for i in code.split():
                print(i)

                step = move_player[i]
                if self.game.check_code_user(step[1]):
                    print('Двигаем')

                    # self.player.move(x_s + step[0][0], x_e + step[0][0])
                else:
                    print('не Двигаем')
            # else:
            #     pobeda.append(user)

        if len(pobeda) == 0:
            pobeda.append('никто не прошёл(')

        slm = QStringListModel()
        slm.setStringList(pobeda)
        self.listView.setModel(slm)
        self.player.hide()

    # Коннект между тг и интерфейсом
    def connect_service(self, resp):
        print(resp)

        if resp['user'] == 'ADMIN':
            if resp['command'] == 'create_code':
                print('123')
                self.code_game_text.setText(self.game.create_code_game())
                slm = QStringListModel()
                slm.setStringList(['Ожидание игроков'])
                self.listView.setModel(slm)

            elif resp['command'] == 'start_game':
                game_num = self.game.start_game()
                pixmap = QPixmap(f'src/static/img/maze/{game_num}.png')
                self.game_place.setPixmap(pixmap)
                self.player.show()


            elif resp['command'] == 'end_game':
                self.game.end_game()
                pixmap = QPixmap(f'src/static/img/maze/0.png')
                self.game_place.setPixmap(pixmap)
                # self.progr = ProgressThread(self.game, self)
                # self.progr.start()
                self.player_shows(self.game.end_game())
                # self.player.hide()

            return

        if resp['command'] == 'enter_the_game':
            print(resp['name'])
        elif resp['command'] == 'register_command':
            print(resp['code'])
            self.game.create_user_code(resp)


def show_inreface():
    print('Старт приложения')

    app = QApplication(sys.argv)

    screen = MainWindow()
    screen.show()
    screen.setWindowTitle('CodeRun')
    # screen.setWindowIcon(QtGui.QIcon('./settings/icon_test.ico'))
    sys.exit(app.exec_())


class ProgressBarThread(QThread):
    # сигналы
    message_update = pyqtSignal(dict)

    def __init__(self, game, interface: MainWindow):
        super().__init__()
        self.game = game
        self.inter = interface
        self.tg = True

    # определяем откуда сигнал
    def run(self):
        if self.tg:
            self.tg = False
            start_tg(self, self.game)
        else:
            print('ИГРААААА')
            self.player_shows(self.game.end_game())

    def player_shows(self, data):
        from time import sleep

        x, y = 40, 40
        move_player = {
            'вверх': [(-y, 0), (-1, 0)],
            'вниз': [(y, 0), (1, 0)],
            'влево': [(-x, 0), (-1, 0)],
            'вправо': [(x, 0), (1, 0)]
        }

        for user, code in data.items():
            x_s, x_e = 35, -20
            print(user)
            for i in code.split():
                print(i)
                sleep(2)
                step = move_player[i]
                if self.game.check_code_user(step[1]):
                    print('Двигаем')
                    self.game.player.move(x_s + step[0][0], x_e + step[0][0])
                else:
                    print('не Двигаем')

            sleep(4)
            self.game.player.hide()


class ProgressThread(QThread):
    # сигналы
    message_update = pyqtSignal(dict)

    def __init__(self, game, interface: MainWindow):
        super().__init__()
        self.game = game
        self.inter = interface

    # определяем откуда сигнал
    def run(self):
            print('ИГРААААА')
            self.player_shows(self.game.end_game())

    def player_shows(self, data):
        from time import sleep

        x, y = 40, 40
        move_player = {
            'вверх': [(-y, 0), (-1, 0)],
            'вниз': [(y, 0), (1, 0)],
            'влево': [(-x, 0), (-1, 0)],
            'вправо': [(x, 0), (1, 0)]
        }

        for user, code in data.items():
            x_s, x_e = 35, -20
            print(user)
            for i in code.split():
                print(i)
                sleep(2)
                step = move_player[i]
                if self.game.check_code_user(step[1]):
                    print('Двигаем')
                    self.game.player.move(x_s + step[0][0], x_e + step[0][0])
                else:
                    print('не Двигаем')

            sleep(4)
            self.game.player.hide()


if __name__ == '__main__':
    show_inreface()
