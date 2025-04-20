"""
GUI implementation for YouTube Auto Backup
"""

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFileDialog
)
from PySide6.QtGui import QLinearGradient, QBrush, QPalette, QColor
from PySide6.QtCore import QThread, Qt

from src.downloader import DownloadWorker


class YouTubeDownloaderApp(QWidget):
    """Main application window for YouTube Auto Backup"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 500, 300)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.threads = {}
        self.elements = {}

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        # Layouts
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Download Path
        path_layout = QHBoxLayout()
        path_label = QLabel("Download Path:")
        self.path_input = QLineEdit(os.path.join(os.getcwd(), 'yt_downloads'))
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_download_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        main_layout.addLayout(path_layout)

        # Input YouTube API
        api_layout = QHBoxLayout()
        api_label = QLabel("Youtube Data Api:")
        self.api_input = QLineEdit("place your Youtube Api here")
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_input)
        main_layout.addLayout(api_layout)

        # Download Main Channel
        main_path_layout = QHBoxLayout()
        main_path_label = QLabel("Download Main Channel")
        self.main_browse_button = QPushButton("Download")
        self.main_browse_button.clicked.connect(self.download_main_channel)
        main_path_layout.addWidget(main_path_label)
        main_path_layout.addWidget(self.main_browse_button)
        main_layout.addLayout(main_path_layout)

        # Download Yellow Channel
        yellow_path_layout = QHBoxLayout()
        yellow_path_label = QLabel("Download Yellow Channel")
        self.yellow_browse_button = QPushButton("Download")
        self.yellow_browse_button.clicked.connect(self.download_yellow_channel)
        yellow_path_layout.addWidget(yellow_path_label)
        yellow_path_layout.addWidget(self.yellow_browse_button)
        main_layout.addLayout(yellow_path_layout)

        # Download Small Channel
        small_path_layout = QHBoxLayout()
        small_path_label = QLabel("Download Small Channel")
        self.small_browse_button = QPushButton("Download")
        self.small_browse_button.clicked.connect(self.download_small_channel)
        small_path_layout.addWidget(small_path_label)
        small_path_layout.addWidget(self.small_browse_button)
        main_layout.addLayout(small_path_layout)

        # Input URL
        url_layout = QHBoxLayout()
        url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.single_video_button = QPushButton("Download Video")
        self.channel_videos_button = QPushButton("Download Channel")
        self.single_video_button.clicked.connect(self.download_video)
        self.channel_videos_button.clicked.connect(self.download_channel)
        button_layout.addWidget(self.single_video_button)
        button_layout.addWidget(self.channel_videos_button)
        main_layout.addLayout(button_layout)

    def browse_download_path(self):
        """Open a dialog to select the download directory"""
        path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if path:
            self.path_input.setText(path)

    def download_video(self):
        """Download a single YouTube video"""
        url = self.url_input.text()
        download_path = self.path_input.text()
        self.elements[url] = self.single_video_button
        self.single_video_button.setEnabled(False)
        if url:
            try:
                self.executor.submit(self.download_video_thread, url, download_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide a valid YouTube URL.")

    def download_channel(self):
        """Download videos from a YouTube channel"""
        url = self.url_input.text()
        self.elements[url] = self.channel_videos_button
        self.channel_videos_button.setEnabled(False)
        api = self.api_input.text()
        download_path = self.path_input.text()
        if url:
            if not 'channel' in url:
                QMessageBox.critical(self, "Input Error", f"Please Enter Valid Channel Url")
            else:
                try:
                    self.executor.submit(self.download_channel_thread, url, api, download_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide a valid YouTube URL.")
    
    def download_main_channel(self):
        """Download videos from the main channel"""
        url = "https://www.youtube.com/channel/UC_4NoVAkQzeSaxCgm-to25A/"  # replace with your channel link
        self.elements[url] = self.main_browse_button
        self.main_browse_button.setEnabled(False)
        api = self.api_input.text()
        download_path = self.path_input.text()
        if url:
            try:
                self.executor.submit(self.download_channel_thread, url, api, download_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide a valid YouTube URL.")

    def download_yellow_channel(self):
        """Download videos from the yellow channel"""
        url = "https://www.youtube.com/channel/UCrOmFbHgf_k4pk-jYRmyhjw/"  # replace with your channel link
        self.elements[url] = self.yellow_browse_button
        self.yellow_browse_button.setEnabled(False)
        api = self.api_input.text()
        download_path = self.path_input.text()
        if url:
            try:
                self.executor.submit(self.download_channel_thread, url, api, download_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide a valid YouTube URL.")

    def download_small_channel(self):
        """Download videos from the small channel"""
        url = "https://www.youtube.com/channel/UC1FfoXAlTmo_jGtTG_bw3bA/"  # replace with your channel link
        self.elements[url] = self.small_browse_button
        self.small_browse_button.setEnabled(False)
        api = self.api_input.text()
        download_path = self.path_input.text()
        if url:
            try:
                self.executor.submit(self.download_channel_thread, url, api, download_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide a valid YouTube URL.")

    def download_video_thread(self, url, download_path):
        """Start a thread to download a single video"""
        thread = QThread()
        self.threads[url] = thread
        worker = DownloadWorker()
        worker.moveToThread(thread)
        worker.finished.connect(self.video_download_complete)
        thread.started.connect(lambda: worker.download_youtube_video(url, download_path))
        thread.start()

    def download_channel_thread(self, url, api, download_path):
        """Start a thread to download a channel's videos"""
        thread = QThread()
        self.threads[url] = thread
        worker = DownloadWorker()
        worker.moveToThread(thread)
        worker.progress.connect(self.update_progress)
        worker.finished.connect(self.channel_download_complete)
        thread.started.connect(lambda: worker.download_channel_videos(url, api, download_path))
        thread.start()

    def update_progress(self, url, progress):
        """Update button text and color dynamically based on progress"""
        # Extract progress values
        current, total = map(int, progress.split('/'))
        ratio = current / total if total > 0 else 0

        # Update button text
        button = self.elements[url]
        button.setText(progress)

        # Create a gradient based on the progress ratio
        gradient = QLinearGradient(0, 0, button.width(), 0)
        gradient.setColorAt(0.0, Qt.green)  # Start with green
        gradient.setColorAt(ratio, Qt.green)  # End green at the progress point
        gradient.setColorAt(ratio, QColor("#1e1e1e"))  # Start default color
        gradient.setColorAt(1.0, QColor("#1e1e1e"))  # End with default

        # Apply gradient to the button
        palette = button.palette()
        palette.setBrush(QPalette.Button, QBrush(gradient))
        button.setPalette(palette)
        button.setAutoFillBackground(True)

    def video_download_complete(self, url):
        """Handle the completion of a video download"""
        button = self.elements.get(url)
        if button:
            button.setEnabled(True)
            
        thread = self.threads.get(url)
        if thread:
            thread.quit()
            thread.wait()
            
        QMessageBox.information(self, "Success", "Video downloaded successfully!")

    def channel_download_complete(self, url):
        """Handle the completion of a channel download"""
        # Stop the thread
        thread = self.threads.get(url)
        if thread:
            thread.quit()
            thread.wait()

        # Update the button to indicate completion
        button = self.elements.get(url)
        if button:
            button.setText("Download complete. Download again?")
            button.setEnabled(True)

            # Change button color to #3c3c3c
            palette = button.palette()
            palette.setColor(QPalette.Button, QColor("#3c3c3c"))
            button.setPalette(palette)
            button.setAutoFillBackground(True)

        # Show a success message
        QMessageBox.information(self, "Success", "Channel downloaded successfully!") 