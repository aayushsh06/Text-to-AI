from pytubefix import YouTube
import moviepy.editor as mp
import os
import tempfile

video_url = 'https://www.youtube.com/watch?v=FzI-c9qRnAo'
filename = "minecraft_gp.mp4"

def download_video(url, temp_file_path):
    try:
        yt = YouTube(url)

        video_streams = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True)

        print("Available video resolutions:")
        for stream in video_streams:
            print(f"Resolution: {stream.resolution}")

        highest_resolution_stream = max(video_streams, key=lambda s: int(s.resolution.strip('p')))

        print(f"\nDownloading: {yt.title}")
        highest_resolution_stream.download(output_path=os.path.dirname(temp_file_path), filename=os.path.basename(temp_file_path))
        print(f"Download complete! Video saved to temporary file: {temp_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def subclip_video(input_path, output_path):
    try:
        video = mp.VideoFileClip(input_path)
        
        duration = video.duration
        half_duration = duration / 2
        
        subclip = video.subclip(0, half_duration)
        
        subclip.write_videofile(output_path, codec='libx264')
        print(f"Subclipped video saved to {output_path}")

    except Exception as e:
        print(f"An error occurred while processing the video: {e}")

def main():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    try:
        download_video(video_url, temp_file_path)
        
        subclip_video(temp_file_path, filename)
    
    finally:
        # Clean up: Delete the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file {temp_file_path} deleted.")

if __name__ == "__main__":
    main()
