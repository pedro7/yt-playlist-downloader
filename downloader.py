from PyQt6.QtWidgets import QApplication, QComboBox, QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import Playlist, YouTube
from sys import exit

def download_playlist(url, resolution, path):
    try:
        playlist = Playlist(url)
        for video in playlist.videos:
            download_video(video.watch_url, resolution, path)
    except:
        download_video(url, resolution, path)
    
def download_video(url, resolution, path):
    video = YouTube(url)
    if resolution == 'Audio Only':
        video.streams.get_audio_only().download(path)
    else:
        video.streams.get_by_resolution(resolution).download(path)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.line = QLineEdit()
        self.line.setPlaceholderText('Paste the playlist/video url')

        self.combo = QComboBox()
        self.combo.addItems(['Audio Only', '720p', '480p', '360p', '240p', '144p'])

        button = QPushButton('Download')
        button.clicked.connect(self.download)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.line)
        layout1.addWidget(self.combo)

        layout2 = QHBoxLayout()
        layout2.addWidget(button)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        self.setWindowTitle('YouTube Downloader')
        self.setFixedSize(300, 74)
        self.setLayout(layout)
        self.show()

    def download(self):
        url = self.line.text()
        resolution = self.combo.currentText()
        path = QFileDialog().getExistingDirectory()
        if path:
            download_playlist(url, resolution, path)

def main():
    app = QApplication([])
    window = Window()
    exit(app.exec())

if __name__ == '__main__':
    main()
