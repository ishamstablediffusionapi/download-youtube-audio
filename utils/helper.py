import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import yt_dlp as YtDl
import re
import os
import subprocess
from datetime import timedelta


def return_youtube_id(url: str):
    """
    Returns YouTube ID of the video.

    Args:
        url: youtube video link
    Returns:
        str: youtube id
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)


def Download_Youtube_Audio(audio_file_path: str, url: str):
    """
    Download YouTube audio given the audio file path and the URL of the video.

    Args:
        audio_file_path (str): The path where the downloaded audio file will be saved.
        url (str): The URL of the YouTube video.

    Returns:
        None
    """
    try:
        youtube_id = return_youtube_id(url)
        video_link = f"https://www.youtube.com/watch?v={youtube_id}"
        ytdl_opts = {
            "format": "mp3/bestaudio/best",
            "source_address": "0.0.0.0",
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
            "outtmpl": f"{audio_file_path}/{youtube_id}",
        }

        with YtDl.YoutubeDL(ytdl_opts) as ydl:
            ydl.cache.remove()
            ydl.download(video_link)
            return None

    except Exception as ex_youtubedl:
        print(f"Youtube > DownloadAudio >> EXCEPTION Youtube_DL:", ex_youtubedl)


def trim_audio(input_file_path: str, start_time: float, end_time: float):
    """
    Trim a video file to a specific start and end time.

    :param input_file_path: The name of the video file to be trimmed.
    :type input_file_path: str
    :param start_time: The start time of the new video in seconds.
    :type start_time: float
    :param end_time: The end time of the new video in seconds.
    :type end_time: float
    """
    # input_file = os.path.join("audio_samples", input_file_path)
    path, file_name = (
        os.path.split(input_file_path)[0],
        os.path.split(input_file_path)[1],
    )
    output_file = os.path.join(path, f"trimmed_{file_name}")

    # Check if input file exists
    if not os.path.exists(input_file_path):
        raise ValueError(f"Input file {input_file_path} does not exist.")

    # Convert start and end times to formatted strings
    start_time = str(timedelta(seconds=start_time))
    end_time = str(timedelta(seconds=end_time))

    # Run ffmpeg command to trim the video
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file_path,
                "-ss",
                start_time,
                "-to",
                end_time,
                output_file,
                "-y",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error trimming video: {e}")

    # Check if output file was created
    if not os.path.exists(output_file):
        raise ValueError(f"Output file {output_file} was not created.")
