"""
YouTube downloader module for handling video and channel downloads
"""

import os
import time
from datetime import datetime
import yt_dlp
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from PySide6.QtCore import QObject, Signal

from src.utils import sanitize_filename, format_filename, delete_https_subfolders, write_to_csv


class DownloadWorker(QObject):
    """Worker class for handling YouTube downloads in a separate thread"""
    
    progress = Signal(str, str)  # Signal to emit progress (current, total)
    finished = Signal(str)  # Signal to notify when download is done

    def __init__(self):
        super().__init__()

    def download_youtube_video(self, url, download_path='yt_downloads', title=None, upload_date=None):
        """
        Download a single YouTube video with its thumbnail and description
        
        Args:
            url (str): YouTube video URL
            download_path (str): Path to download directory
            title (str, optional): Video title (for channel downloads)
            upload_date (str, optional): Upload date (for channel downloads)
            
        Returns:
            None
        """
        download_path = os.path.abspath(download_path)
        delete_https_subfolders(download_path)
        ischannel = False

        if title and upload_date:
            ischannel = True
            upload_date = datetime.strptime(upload_date, "%Y-%m-%dT%H:%M:%SZ")
            mp4file = os.path.join(download_path, format_filename(upload_date, title, 'mp4'))
            if os.path.exists(mp4file):
                return

        download_folder = os.path.join(download_path, sanitize_filename(url))
        if not os.path.exists(download_folder):
            os.makedirs(download_folder, exist_ok=True)
        else:
            folder_exsist = True
            times = 0
            while folder_exsist:
                time.sleep(3)
                if not os.path.exists(download_folder):
                    folder_exsist = False
                if times >= 5:
                    os.removedirs(download_folder)
                    folder_exsist = False
                times += 1
                
        e_num = 0
        while True:
            try:
                ydl_opts = {
                    'outtmpl': os.path.join(download_folder, 'files.%(ext)s'),
                    'format': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4][height=1080]',
                    'writedescription': True,
                    'writethumbnail': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    if not ischannel:
                        info = ydl.extract_info(url, download=False)
                        title = info.get('title')
                        upload_date = datetime.strptime(info['upload_date'], "%Y%m%d")
                        video_ext = info.get('ext')
                        new_video_name = format_filename(upload_date, title, video_ext)
                        if os.path.exists(os.path.join(download_path, new_video_name)):
                            self.finished.emit(url)
                            return

                    info = ydl.extract_info(url, download=True)
                    title = info.get('title')
                    upload_date = datetime.strptime(info['upload_date'], "%Y%m%d")

                    # Rename downloaded video file
                    video_ext = info.get('ext')
                    video_path = os.path.join(download_folder, f"files.{video_ext}")
                    new_video_name = format_filename(upload_date, title, video_ext)
                    print("new video name:", new_video_name)
                    os.makedirs(os.path.dirname(os.path.join(download_path, new_video_name)), exist_ok=True)
                    shutil.move(video_path, os.path.join(download_path, new_video_name))
                    print(f"Downloaded video: {new_video_name}")
                    
                    # Rename downloaded thumbnail
                    thumbnail_path = os.path.join(download_folder, f"files.webp")
                    if os.path.exists(thumbnail_path):
                        new_thumbnail_name = format_filename(upload_date, title, "jpg")
                        shutil.move(thumbnail_path, os.path.join(download_path, new_thumbnail_name))
                        print(f"Downloaded thumbnail: {new_thumbnail_name}")

                    # Rename description info to .txt
                    txt_path = os.path.join(download_folder, f"files.description")
                    if os.path.exists(txt_path):
                        new_description_name = format_filename(upload_date, title, "txt")
                        shutil.move(txt_path, os.path.join(download_path, new_description_name))
                        print(f"Saved description as: {new_description_name}")
                    break
            except Exception as e:
                print(str(e))
                if e_num == 0:
                    ydl_opts = {
                        'outtmpl': os.path.join(download_folder, 'files.%(ext)s'),
                        'format': 'bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/best[ext=mp4][height=720]',
                        'writedescription': True,
                        'writethumbnail': True
                    }
                elif e_num == 1:
                    ydl_opts = {
                        'outtmpl': os.path.join(download_folder, 'files.%(ext)s'),
                        'format': 'best',
                        'writedescription': True,
                        'writethumbnail': True
                    }
                elif e_num == 5:
                    if not ischannel:
                        self.finished.emit(url) 
                    return
                e_num += 1
        
        if os.path.exists(download_folder):
            import shutil
            shutil.rmtree(download_folder)
        if not ischannel:
            self.finished.emit(url)        

    def download_channel_videos(self, channel_url, api_key, download_path='yt_downloads'):
        """
        Download all videos from a YouTube channel
        
        Args:
            channel_url (str): YouTube channel URL
            api_key (str): YouTube Data API key
            download_path (str): Path to download directory
            
        Returns:
            None
        """
        uploads_playlist_id, channel_name = self.get_channel_uploads_playlist_id(channel_url, api_key)
        channel_folder = os.path.join(download_path, sanitize_filename(channel_name))
        if not os.path.exists(channel_folder):
            os.makedirs(channel_folder, exist_ok=True)
        download_path = channel_folder
        
        if uploads_playlist_id:
            # Get all videos from the uploads playlist
            videos = self.get_all_videos_from_playlist(uploads_playlist_id, api_key)
            print(f"Total videos found: {len(videos)}\n")
        else:
            print("Failed to retrieve uploads playlist ID.")
            self.finished.emit(channel_url)
            return

        for i, video in enumerate(videos):
            self.progress.emit(channel_url, f"{i+1}/{len(videos)}")
            self.download_youtube_video(video['url'], download_path, video['title'], video['upload_date'])
            
            # Write data to the CSV file
            csv_file_path = os.path.abspath("video_data.csv")
            write_to_csv(csv_file_path, channel_name, video['title'], video['url'])

        self.finished.emit(channel_url)

    def download_video(self, video, download_path, download_function):
        """
        Wrapper function to download a video.
        
        Args:
            video (dict): Video information
            download_path (str): Path to download directory
            download_function (function): Function to use for downloading
            
        Returns:
            str: Video URL
        """
        video_link = video['url']
        download_function(video_link, download_path)
        return video_link

    def parallel_download(self, videos, download_path, download_function, progress_signal, url):
        """
        Downloads videos in parallel using ThreadPoolExecutor.
        
        Args:
            videos (list): List of videos to download
            download_path (str): Path to download directory
            download_function (function): Function to use for downloading
            progress_signal (Signal): Signal to emit progress
            url (str): Channel URL
        """
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.download_video, video, download_path, download_function): i
                for i, video in enumerate(videos)
            }

            for future in as_completed(futures):
                i = futures[future]
                try:
                    result = future.result()
                    progress_signal.emit(url, f"{i + 1}/{len(videos)}")
                except Exception as e:
                    progress_signal.emit(url, f"{i + 1}/{len(videos)}")

    def get_channel_uploads_playlist_id(self, channel_url, api_key):
        """
        Fetch the Uploads playlist ID of the channel.
        
        Args:
            channel_url (str): YouTube channel URL
            api_key (str): YouTube Data API key
            
        Returns:
            tuple: (uploads_playlist_id, channel_name) or (None, None)
        """
        channel_id = ''
        try:
            parsed_url = urlparse(channel_url)
            # Check if the URL contains '/channel/'
            if "/channel/" in parsed_url.path:
                channel_id = parsed_url.path.split("/channel/")[1].strip("/")
            else:
                print("Invalid URL or not a direct channel URL.")
                return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None
        
        base_url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "snippet,contentDetails",
            "id": channel_id,
            "key": api_key
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        try:
            uploads_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            channel_name = data["items"][0]["snippet"]["title"]
            return uploads_playlist_id, channel_name
        except (KeyError, IndexError):
            print("Error: Could not find uploads playlist.")
            return None, None

    def get_all_videos_from_playlist(self, playlist_id, api_key):
        """
        Fetch all video titles, links, and upload dates from the playlist with parallel requests.
        
        Args:
            playlist_id (str): YouTube playlist ID
            api_key (str): YouTube Data API key
            
        Returns:
            list: List of video information dictionaries
        """
        base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        max_results_per_request = 50

        def fetch_page(page_token=None):
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": max_results_per_request,
                "key": api_key,
                "pageToken": page_token,
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()

        # Fetch the first page to get total items and nextPageToken
        initial_data = fetch_page()
        videos = []

        # Collect video details from the initial page
        for item in initial_data["items"]:
            title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            upload_date = item["snippet"]["publishedAt"]  # ISO 8601 format
            videos.append({"title": title, "url": video_url, "upload_date": upload_date})

        next_page_token = initial_data.get("nextPageToken")

        # Collect all subsequent page tokens
        page_tokens = []
        while next_page_token:
            page_tokens.append(next_page_token)
            next_page_data = fetch_page(next_page_token)
            next_page_token = next_page_data.get("nextPageToken")

        # Define a function to fetch a single page's videos
        def fetch_and_parse_videos(page_token):
            data = fetch_page(page_token)
            page_videos = []
            for item in data["items"]:
                title = item["snippet"]["title"]
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                upload_date = item["snippet"]["publishedAt"]  # ISO 8601 format
                page_videos.append({"title": title, "url": video_url, "upload_date": upload_date})
            return page_videos

        # Use ThreadPoolExecutor to fetch videos concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_token = {executor.submit(fetch_and_parse_videos, token): token for token in page_tokens}
            for future in as_completed(future_to_token):
                try:
                    videos.extend(future.result())
                except Exception as e:
                    print(f"Error fetching page: {e}")

        return videos 