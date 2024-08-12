import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import os
import subprocess
import platform
import time
import threading
from pydub import AudioSegment

# Define a function to get the default download path based on the operating system
def get_default_downloads_path():
    if platform.system() == 'Windows':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                downloads_path = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
            return downloads_path
        except:
            return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def generate_unique_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1

    return unique_filename

def download_video_as_mp3(url, download_path, progress_callback, trim=False, start_time=0, end_time=0):
    os.makedirs(download_path, exist_ok=True)

    def progress_hook(d):
        if d['status'] == 'downloading':
            progress_callback(f"Downloading: {d.get('_percent_str', '0%')}")
        elif d['status'] == 'finished':
            progress_callback("Download finished. Converting to MP3...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        filename = os.path.splitext(filename)[0] + '.mp3'
    
    unique_filename = generate_unique_filename(download_path, os.path.basename(filename))
    unique_filepath = os.path.join(download_path, unique_filename)
    os.rename(filename, unique_filepath)
    
    if trim and start_time < end_time:
        progress_callback("Trimming audio...")
        audio = AudioSegment.from_mp3(unique_filepath)
        trimmed_audio = audio[start_time*1000:end_time*1000]
        trimmed_filename = generate_unique_filename(download_path, os.path.splitext(unique_filename)[0] + '_trimmed.mp3')
        trimmed_filepath = os.path.join(download_path, trimmed_filename)
        trimmed_audio.export(trimmed_filepath, format="mp3")
        os.remove(unique_filepath)
        unique_filepath = trimmed_filepath

    current_time = time.time()
    os.utime(unique_filepath, (current_time, current_time))
    
    return unique_filepath

def open_file(filepath):
    if platform.system() == 'Darwin':
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':
        os.startfile(filepath)
    else:
        subprocess.call(('xdg-open', filepath))

class YouTubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube MP3 Downloader")
        master.geometry("400x350")

        self.url_label = tk.Label(master, text="Enter YouTube URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack(pady=5)

        self.path_label = tk.Label(master, text="Download Path:")
        self.path_label.pack(pady=5)

        self.path_entry = tk.Entry(master, width=50)
        self.path_entry.pack(pady=5)
        self.path_entry.insert(0, get_default_downloads_path())

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_path)
        self.browse_button.pack(pady=5)

        self.trim_var = tk.BooleanVar()
        self.trim_check = tk.Checkbutton(master, text="Trim audio", variable=self.trim_var, command=self.toggle_trim_options)
        self.trim_check.pack(pady=5)

        self.trim_frame = tk.Frame(master)
        self.trim_frame.pack(pady=5)

        self.start_label = tk.Label(self.trim_frame, text="Start time (s):")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(self.trim_frame, width=10)
        self.start_entry.grid(row=0, column=1)

        self.end_label = tk.Label(self.trim_frame, text="End time (s):")
        self.end_label.grid(row=0, column=2)
        self.end_entry = tk.Entry(self.trim_frame, width=10)
        self.end_entry.grid(row=0, column=3)

        self.trim_frame.pack_forget()

        self.download_button = tk.Button(master, text="Download", command=self.start_download)
        self.download_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=5)

    def toggle_trim_options(self):
        if self.trim_var.get():
            self.trim_frame.pack(pady=5)
        else:
            self.trim_frame.pack_forget()

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_download(self):
        url = self.url_entry.get()
        path = self.path_entry.get()

        if not url or not path:
            messagebox.showerror("Error", "Please enter both URL and download path.")
            return

        trim = self.trim_var.get()
        start_time = 0
        end_time = 0

        if trim:
            try:
                start_time = float(self.start_entry.get())
                end_time = float(self.end_entry.get())
                if start_time >= end_time:
                    raise ValueError("End time must be greater than start time.")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid trim times: {str(e)}")
                return

        self.download_button.config(state=tk.DISABLED)
        threading.Thread(target=self.download_thread, args=(url, path, trim, start_time, end_time), daemon=True).start()

    def download_thread(self, url, path, trim, start_time, end_time):
        try:
            def update_status(status):
                self.status_label.config(text=status)

            filename = download_video_as_mp3(url, path, update_status, trim, start_time, end_time)
            self.master.after(0, lambda: self.download_complete(filename))
        except Exception as e:
            # Properly pass the exception message to the error handling function
            self.master.after(0, lambda e=e: self.download_error(str(e)))


    def download_complete(self, filename):
        self.status_label.config(text="Download complete!")
        self.download_button.config(state=tk.NORMAL)
        if messagebox.askyesno("Download Complete", f"File downloaded: {filename}\nDo you want to open it?"):
            open_file(filename)

    def download_error(self, error_message):
        self.status_label.config(text="Download failed")
        self.download_button.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"An error occurred: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()