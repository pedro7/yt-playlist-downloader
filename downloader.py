from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import Channel, Playlist, YouTube
from sys import exit

class DownloadWorker(QObject):
    progress = pyqtSignal(str)
    complete = pyqtSignal(str)

    def download(self, url, resolution, format, path):
        try:
            self.download_video(url, resolution, format, path)
        except:
            self.download_videos(url, resolution, format, path)
        self.complete.emit('No downloads queued')

    def download_videos(self, url, resolution, format, path):
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                self.download_video(video.watch_url, resolution, format, path)
        except:
            channel = Channel(url)
            for video in channel.videos:
                self.download_video(video.watch_url, resolution, format, path)

    def download_video(self, url, resolution, format, path):
        video = YouTube(url)
        self.progress.emit(f'Downloading: {video.title}')
        if resolution == 'Audio Only':
            video.streams.get_audio_only().download(path)
        elif resolution == 'Highest Resolution':
            video.streams.get_highest_resolution().download(path)
        else:
            video.streams.get_lowest_resolution().download(path)

class Downloader(QWidget):
    download_requested = pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()
        self.create_gui()

    def create_gui(self):
        self.line = QLineEdit()
        self.line.setPlaceholderText('Paste the video/playlist/channel url')

        self.combo = QComboBox()
        self.combo.addItems(['Audio Only', 'Highest Resolution', 'Lowest Resolution'])

        self.button = QPushButton('Download')
        self.button.clicked.connect(self.download)

        self.label = QLabel('No downloads queued')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.line)
        top_layout.addWidget(self.combo)

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.button)
        bottom_layout.addWidget(self.label)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)

        self.setWindowTitle('YouTube Downloader')
        self.setFixedSize(500, 96)
        self.setLayout(layout)
        self.show()

    def download(self):
        path = QFileDialog().getExistingDirectory()

        if not path:
            return

        self.button.setEnabled(False)

        self.worker = DownloadWorker()
        self.thread = QThread()

        self.worker.moveToThread(self.thread)

        self.download_requested.connect(self.worker.download)
        self.worker.progress.connect(self.update_label)
        self.worker.complete.connect(self.update_label)
        self.worker.complete.connect(lambda: self.button.setEnabled(True))

        self.thread.start()

        url = self.line.text()
        resolution = self.combo.currentText()
        self.download_requested.emit(url, resolution, '', path)

    def update_label(self, text):
        self.label.setText(text)

def app():
    app = QApplication([])
    app.setStyle('Fusion')
    downloader = Downloader()
    exit(app.exec())

if __name__ == '__main__':
    app()
