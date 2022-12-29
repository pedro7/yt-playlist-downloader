from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import Playlist, YouTube
from sys import exit

class DownloadWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)

    def download_playlist(self, url, resolution, path):
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                self.download_video(video.watch_url, resolution, path)
        except:
            self.download_video(url, resolution, path)
        self.finished.emit('No downloads queued')
    
    def download_video(self, url, resolution, path):
        video = YouTube(url)
        self.progress.emit(f'Downloading: {video.title}')
        if resolution == 'Audio Only':
            video.streams.get_audio_only().download(path)
        else:
            video.streams.get_by_resolution(resolution).download(path)

class Downloader(QWidget):
    download_requested = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.line = QLineEdit()
        self.line.setPlaceholderText('Paste the playlist/video url')

        self.combo = QComboBox()
        self.combo.addItems(['Audio Only', '720p', '480p', '360p', '240p', '144p'])

        self.button = QPushButton('Download')
        self.button.clicked.connect(self.download)

        self.label = QLabel('No downloads queued')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.line)
        layout1.addWidget(self.combo)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.button)
        layout2.addWidget(self.label)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        self.setWindowTitle('YouTube Downloader')
        self.setFixedSize(400, 96)
        self.setLayout(layout)
        self.show()

    def download(self):
        url = self.line.text()
        resolution = self.combo.currentText()
        path = QFileDialog().getExistingDirectory()
        
        if not path:
            return

        self.button.setEnabled(False)

        self.worker = DownloadWorker()
        self.thread = QThread()

        self.worker.moveToThread(self.thread)

        self.download_requested.connect(self.worker.download_playlist)
        self.worker.progress.connect(self.update_label)
        self.worker.finished.connect(self.update_label)
        self.worker.finished.connect(lambda: self.button.setEnabled(True))

        self.thread.start()

        self.download_requested.emit(url, resolution, path)

    def update_label(self, text):
        self.label.setText(text)

def main():
    app = QApplication([])
    downloader = Downloader()
    exit(app.exec())

if __name__ == '__main__':
    main()
