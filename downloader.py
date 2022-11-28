from pytube import Playlist, YouTube

def download_playlist(url, path):
    try:
        playlist = Playlist(url)
        for video in playlist.videos:
            download_video(video.watch_url, path)
    except:
        download_video(url, path)
    
def download_video(url, path):
    video = YouTube(url)
    print(f'Downloading: {video.title}')
    video.streams.get_audio_only().download(path)

def main():
    path = input("Enter the path to where you'd like to save: ")
    while True:
        url = input('Enter the playlist/video url: ')
        print()
        download_playlist(url, path)
        print('Download completed\n')

if __name__ == '__main__':
    main()