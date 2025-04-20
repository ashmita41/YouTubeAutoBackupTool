# 📝 YouTube Auto Backup - Usage Guide

This guide explains how to use the YouTube Auto Backup application effectively.

## 🚀 Starting the Application

To start the application, run the following command from the repository root:

```bash
python -m youtube_backup.main
```

## 🔑 YouTube Data API Key

To download videos from channels, you need a YouTube Data API key. 

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to APIs & Services > Library
4. Search for "YouTube Data API v3" and enable it
5. Go to APIs & Services > Credentials
6. Create an API key and copy it
7. Paste the API key into the "YouTube Data API" field in the application

## 💾 Downloading Videos

### Single Video Download

1. Copy the YouTube video URL
2. Paste it into the "YouTube URL" field
3. Click the "Download Video" button
4. The video will be downloaded to the specified download path

### Channel Download

1. Copy the YouTube channel URL (must be in the format `https://www.youtube.com/channel/CHANNEL_ID`)
2. Paste it into the "YouTube URL" field
3. Make sure your YouTube Data API key is entered
4. Click the "Download Channel" button
5. The videos will be downloaded to a subfolder named after the channel

## 🔄 Preconfigured Channels

The application has three preconfigured channel buttons:

1. **Main Channel** - Downloads videos from a specific channel
2. **Yellow Channel** - Downloads videos from another specific channel
3. **Small Channel** - Downloads videos from a third specific channel

These buttons can be customized in the code to point to your frequently backed-up channels.

## 📂 Download Path

You can change the download location by:

1. Clicking the "Browse" button
2. Selecting your desired download folder
3. The path will be updated in the text field

## 📊 Download Progress

When downloading channel videos:

1. The button will show the progress (e.g., "15/50")
2. A green progress bar will fill the button as downloads complete
3. When finished, a success message will appear

## 🗂️ Folder Structure

Downloaded videos are organized as follows:

```
download_path/
├── channel_name_1/
│   ├── DD-MM-YYYY - Video Title.mp4
│   ├── DD-MM-YYYY - Video Title.jpg (thumbnail)
│   └── DD-MM-YYYY - Video Title.txt (description)
├── channel_name_2/
│   └── ...
└── DD-MM-YYYY - Single Video Title.mp4 (direct video downloads)
```

## 📋 CSV Records

The application keeps a record of all downloaded videos in a CSV file named `video_data.csv` in the application directory. This contains:

- Channel Name
- Video Title
- Video URL 