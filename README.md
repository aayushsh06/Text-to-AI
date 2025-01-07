# Text-to-AI

### What is it?
The "Text-to-AI" app (formerly known as Brainrot-to-AI) automates the creation of viral-style videos inspired by content on platforms like YouTube and TikTok. These videos feature AI-generated voiceovers reading scripts (e.g., Reddit stories) with synchronized captions and randomly selected background visuals. 

### Steps to use: 
1. Download all files 
2. Install all neccessary APIs and libraries using `requirements.txt`
3. In order to use auto story/brainrot generation, a `GROQ API KEY` must be included (can be obtained for free)
4. In order to use to reddit story generation, a `PRAW key` must be obtained and setup by filling in the associated fields in `reddit.py`
5. Before generating videos, you must download a `.mp4` video for your background and input the filename in `combine.py` (To download a YT video, `personalDownload.py` can be used by inserting the YT vid link and running `python3 personalDownload.py`)


- All code was run on a `Python 3.10.15` virtual environment


## Repository File Descriptions

### `app.py`
The main application script responsible for orchestrating the entire video creation process.

### `TTS.py`
Handles text-to-speech conversion and generates AI voiceovers for the scripts.

### `genScript.py`
Generates scripts for videos, with the ability to source content from Reddit or other platforms.

### `reddit.py`
Facilitates interaction with the Reddit API to fetch stories or posts used in video content.

### `createVid.py`
Combines the script, AI voiceover, synchronized captions, and visual assets to produce a complete video.

### `makeCaption.py`
Creates captions that are perfectly synchronized with the AI-generated voiceover.

### `combine.py`
Merges all media elements, including audio, video, and captions, into the final video output.

### `requirements.txt`
Contains a list of required Python libraries and dependencies necessary to run the application.

### `inputText.txt`
Stores input text or scripts that serve as the basis for video generation.

### `subreddit.txt`
Lists subreddit names or topics to guide the sourcing of content.

### `model.txt`
Holds model configurations or settings for AI processing.

### `personalDownload.py`
A utility script for downloading personal content or assets needed during the video creation process.

