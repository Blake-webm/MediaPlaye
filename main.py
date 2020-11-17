from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel,\
    QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QKeySequence
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QShortcut, QWidget, QPushButton
import sys


def end():
    sys.exit(app.exec_())


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Медиа плеер")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon("Плеер.jpg"))

        # обьект создания Медиа плеера
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # создоем кнопку проигрования
        self.playBtn = QPushButton()

        # создает кнопку открытия
        self.openBtn = QPushButton("Выберите видео")

        # создаем гарячию клавишу выбора видео
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)

        # создаем горячию клавишу выхода
        self.exit = QShortcut(QKeySequence("Esc"), self)

        # создаем горячию клавишу проигрывания видео
        self.playn = QShortcut(QKeySequence("Ctrl+ "), self)

        # создаем палзунок видео
        self.slider = QSlider(Qt.Horizontal)

        # создаем лейбл
        self.lebel = QLabel()

        # создаем hbox
        self.hboxLayot = QHBoxLayout()

        # создаем vbox
        self.vboxLayout = QVBoxLayout()

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):

        # coздаем видео обьект или типо того
        videowidget = QVideoWidget()

        # настройка кнопку открытия
        self.openBtn.clicked.connect(self.open_file)

        # настраеваем кнопку проигрования
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # настраеваем гарячию клавишу выбора видео
        self.shortcut.activated.connect(self.open_file)

        # настраеваем горячию клавишу выхода
        self.exit.activated.connect(end)

        # настраеваем горячию клавишу проигрывания видео
        self.playn.activated.connect(self.play_video)

        # настраеваем палзунок видео
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # настраеваем лейбл
        self.lebel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # настройка hbox
        self.hboxLayot.setContentsMargins(0, 0, 0, 0)

        # создаем виджет hbox
        self.hboxLayot.addWidget(self.openBtn)
        self.hboxLayot.addWidget(self.playBtn)
        self.hboxLayot.addWidget(self.slider)

        # настройка vbox
        self.vboxLayout.addWidget(videowidget)
        self.vboxLayout.addLayout(self.hboxLayot)
        self.vboxLayout.addWidget(self.lebel)

        # сигнал в плеер
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_ch)
        self.setLayout(self.vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть видео")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_ch(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handel_erroros(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Фоталка: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
