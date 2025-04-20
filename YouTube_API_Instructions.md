# Getting a YouTube Data API Key

This guide explains how to obtain a YouTube Data API key for use with YouTubeAutoBackupTool.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Log in with your Google account
3. Click "Create Project" at the top of the page
4. Enter a name for your project (e.g., "YouTubeAutoBackupTool")
5. Click "Create"

## Step 2: Enable the YouTube Data API

1. Wait for your project to be created, then select it from the project dropdown
2. Navigate to "APIs & Services" > "Library" from the left menu
3. Search for "YouTube Data API v3"
4. Click on the API from the search results
5. Click "Enable"

## Step 3: Create API Credentials

1. After enabling the API, click "Create Credentials"
2. For "Which API are you using?" select "YouTube Data API v3"
3. For "Where will you be calling the API from?" select "Web browser (JavaScript)"
4. For "What data will you be accessing?" select "Public data"
5. Click "Next"
6. Enter a name for your API key (e.g., "YouTubeAutoBackupTool Key")
7. Click "Create"

## Step 4: Retrieve and Secure Your API Key

1. Your API key will be displayed. Copy this key.
2. (Optional but recommended) Click "Restrict Key" to limit usage to only the YouTube Data API
3. Under "API restrictions", select "Restrict key"
4. Choose "YouTube Data API v3" from the dropdown
5. Click "Save"

## Step 5: Use Your API Key in YouTubeAutoBackupTool

1. Start the YouTubeAutoBackupTool application
2. Paste your API key into the "YouTube Data API" field
3. You're now ready to download YouTube channels!

## API Quota Information

The YouTube Data API has usage limits:
- Each project has a default quota of 10,000 units per day
- Different operations consume different amounts of quota:
  - Getting video details: ~1-3 units per video
  - Channel listing: ~1 unit
  - Search: ~100 units
  - Video upload: ~1600 units

If you reach your quota limit and need more, you can request additional quota through the Google Cloud Console.

## Troubleshooting

If you encounter errors like "API key not valid" or "Quota exceeded":
1. Make sure you've enabled the YouTube Data API for your project
2. Check that you're using the correct API key
3. Verify your API key is not restricted to specific IPs or referrers
4. Check your quota usage in the Google Cloud Console under "APIs & Services" > "YouTube Data API v3" > "Quotas" 