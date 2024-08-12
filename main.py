from yt_dlp import YoutubeDL
import os
import subprocess
import platform
import time

def download_video_as_mp3(url, download_path):
    # Ensure the download path exists
    os.makedirs(download_path, exist_ok=True)

    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }

    # Download the video
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # Change the extension to mp3
        filename = os.path.splitext(filename)[0] + '.mp3'
    
    # Update file's modification time to current time
    current_time = time.time()
    os.utime(filename, (current_time, current_time))
    
    return filename

def open_file(filepath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter the YouTube video URL: ")
    custom_path = "D:\Downloads"
    
    # Use current directory if no path is provided
    if not custom_path:
        custom_path = os.getcwd()
    
    downloaded_file = download_video_as_mp3(video_url, custom_path)
    print(f"File downloaded: {downloaded_file}")
    
    # Open the file
    open_file(downloaded_file)
    print(f"Opened file: {downloaded_file}")