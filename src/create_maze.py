import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QFileSystemWatcher


class Maze(QWidget):

    def __init__(self, maze_file):
        super().__init__()

        self.maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                self.maze.append(line.strip())

        self.width = len(self.maze[0])
        self.height = len(self.maze)

        # self.file_watcher = QFileSystemWatcher()
        # self.file_watcher.fileChanged.connect(self.refresh_canvas)
        # self.file_watcher.addPath(self.filename)


        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 1000)
        self.setWindowTitle('Maze')
        self.show()

    def paintEvent(self, event):
        try:
            qp = QPainter()
            qp.begin(self)
            self.drawMaze(qp)
            qp.end()
        except Exception as e:
            print(e)

    def drawMaze(self, qp):

        qp.setPen(QPen(Qt.black, 1))
        qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == '1':
                    qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                    qp.drawRect(50 * x, 50 * y, 50, 50)
                elif self.maze[y][x] == '0':
                    qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    qp.drawRect(50 * x, 50 * y, 50, 50)

    # def keyPressEvent(self, event):
    #
    #     key = event.key()
    #     x = self.width // 2
    #     y = self.height // 2
    #
    #     if key == Qt.Key_Left and self.maze[y][x-1] == '-':
    #         self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
    #         self.maze[y] = self.maze[y][:x-1] + '-' + self.maze[y][x:]
    #         self.update()
    #
    #     elif key == Qt.Key_Right and self.maze[y][x+1] == '-':
    #         self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
    #         self.maze[y] = self.maze[y][:x+1] + '-' + self.maze[y][x+2:]
    #         self.update()
    #
    #     elif key == Qt.Key_Up and self.maze[y-1][x] == '-':
    #         self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
    #         self.maze[y-1] = self.maze[y-1][:x] + '-' + self.maze[y-1][x+1:]
    #         self.update()
    #
    #     elif key == Qt.Key_Down and self.maze[y+1][x] == '-':
    #         self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
    #         self.maze[y+1] = self.maze[y+1][:x] + '-' + self.maze[y+1][x+1:]
    #         self.update()


if __name__ == '__main__':
    while True:
        app = QApplication(sys.argv)
        ex = Maze('static/img/maze/10.txt')
        sys.exit(app.exec_())