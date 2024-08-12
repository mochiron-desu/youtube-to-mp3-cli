# YouTube to MP3 CLI

This repository provides a simple command-line interface (CLI) and graphical user interface (GUI) to download and convert YouTube videos to MP3 files. The code leverages the `yt-dlp` library for downloading and `pydub` for optional trimming of audio files.

## Features

- **Download YouTube videos as MP3**: Extract the audio from YouTube videos and save them as MP3 files.
- **Customizable download path**: Choose where the MP3 files will be saved.
- **Trim audio**: Option to trim the downloaded MP3 to a specified start and end time.
- **Cross-platform support**: Works on Windows, macOS, and Linux.

## Installation

### Prerequisites

- Python 3.x
- `yt-dlp` and `pydub` Python libraries
- `FFmpeg` installed on your system for audio processing

### Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/youtube-to-mp3-cli.git
    cd youtube-to-mp3-cli
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure `FFmpeg` is installed and accessible from your system's PATH.**

    - You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Usage

### Command-Line Interface (CLI)

1. **Run the script:**

    ```bash
    python main.py
    ```

2. **Enter the YouTube URL and choose the download path.** The MP3 file will be downloaded and saved to the specified directory.

### Graphical User Interface (GUI)

1. **Run the executable script:**

    ```bash
    python executable.py
    ```

2. **A GUI window will open:**

    - Enter the YouTube URL in the provided field.
    - Select the download path using the "Browse" button.
    - (Optional) Check the "Trim audio" option and specify the start and end times if you want to trim the MP3.
    - Click "Download" to start the process.

## Building the Executable

To build a standalone executable of the application:

1. **Ensure PyInstaller is Installed**

   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable**

   ```bash
   pyinstaller executable.py --onefile --windowed
   ```

   The executable will be available in the `dist` directory.

## Customization

### Modify the script

- **Download format and quality**: You can adjust the `ydl_opts` dictionary in `executable.py` to change the download format or audio quality.
- **Trim functionality**: Adjust the trimming logic in the `download_video_as_mp3` function to customize how the trimming is handled.

## Contributing

Feel free to fork this repository, submit issues, or create pull requests. Contributions are welcome!

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

---

By following these instructions, you should be able to install, configure, and use the YouTube to MP3 downloader. Enjoy!

```
pyinstaller --onefile --windowed .\execulable.py
```
