import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import pysrt

video = VideoFileClip("minecraft_gp.mp4") #Change Filename Based on Your Download

def time_to_seconds(time_obj):
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6

def create_subtitle_clip(sub, video_width):
    start_seconds = time_to_seconds(sub.start.to_time())
    end_seconds = time_to_seconds(sub.end.to_time())
    
    duration_seconds = end_seconds - start_seconds
    
    return (
        TextClip(
            sub.text,
            font="Impact",  
            fontsize=60,
            color="white",
            stroke_width=2,
            stroke_color="black"
        )
        .set_position(("center", "center"))
        .set_start(start_seconds)
        .set_duration(duration_seconds)
    )

audio = AudioFileClip("story.mp3")  

audio_duration = audio.duration
video_duration = video.duration

start_time = random.uniform(0, video_duration - audio_duration)

video_trimmed = video.subclip(start_time, start_time + audio_duration)

video_height = video_trimmed.size[1]
video_width = video_trimmed.size[0]
new_width = int(video_height * 9 / 16)

x_offset = (video_width - new_width) // 2

video_cropped = video_trimmed.crop(x1=x_offset, x2=x_offset + new_width)

video_with_audio = video_cropped.set_audio(audio)

subtitles = pysrt.open("subtitles.srt")

subtitle_clips = []
for sub in subtitles:
    subtitle_clip = create_subtitle_clip(sub, video_with_audio.size[0])
    if subtitle_clip:
        subtitle_clips.append(subtitle_clip)

video_with_subtitles = CompositeVideoClip([video_with_audio] + subtitle_clips)

video_with_subtitles.write_videofile("fullVid.mp4", codec="libx264", audio_codec="aac", fps=30)
