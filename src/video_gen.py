from moviepy import *
import os
from config import VIDEO_DIR, IMAGE_DIR, AUDIO_DIR

def generate_video(image, audio, text, filename):
    audio_path = os.path.join(AUDIO_DIR, audio)
    image_path = os.path.join(IMAGE_DIR, image)

    audio_clip = AudioFileClip(audio_path)

    image_clip = ImageClip(image_path)
    image_clip = image_clip.with_duration(audio_clip.duration)

    text_clip = TextClip(font="Impact", text=text.strip(), font_size=40, color='White', bg_color='Black')
    text_clip = text_clip.with_position(("center", "center"))
    text_clip = text_clip.with_duration(audio_clip.duration)

    video = CompositeVideoClip([image_clip, text_clip])
    video.audio = audio_clip

    save_path = os.path.join(VIDEO_DIR, filename)
    video.write_videofile(save_path, codec="libx264", fps=1)

def merge_video_clips(filename):
    videos = os.listdir(VIDEO_DIR)
    videos.sort()
    video_clips = [VideoFileClip(f"data/videos/{video}") for video in videos]
    final_clip = concatenate_videoclips(video_clips)

    save_path = os.path.join(VIDEO_DIR, filename)
    final_clip.write_videofile(save_path, codec="libx264", fps=1)

if __name__ == "__main__":
    # image = "image_0.png"
    # audio = "audio_0_0.mp3"
    # text = "This is a sample video generated using the AI model."
    # generate_video(image, audio, text, "output.mp4")
    merge_video_clips("final_output.mp4")