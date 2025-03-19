from moviepy import *
import os
from config import VIDEO_DIR, IMAGE_DIR, AUDIO_DIR, OUTPUT_DIR

def generate_video(image, audio, text, filename):
    audio_path = os.path.join(AUDIO_DIR, audio)
    image_path = os.path.join(IMAGE_DIR, image)

    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.with_speed_scaled(factor=1.2)

    if audio_clip.duration - 0.2 > 1:
        audio_clip = audio_clip.subclipped(0, -0.2)

    image_clip = ImageClip(image_path)
    image_clip = image_clip.with_duration(audio_clip.duration)

    text_clip = TextClip(font="Impact", text="\n" + " "+text.strip().replace("\n", "")+" "+"\n", font_size=40, color='White', bg_color='Black')
    text_clip = text_clip.with_position(("center", "center"))
    text_clip = text_clip.with_duration(audio_clip.duration)

    video = CompositeVideoClip([image_clip, text_clip])
    video.audio = audio_clip

    save_path = os.path.join(VIDEO_DIR, filename)
    video.write_videofile(save_path, codec="libx264", fps=10)

def merge_video_clips(filename):
    videos = os.listdir(VIDEO_DIR)
    videos.sort()
    video_clips = []
    for video in videos:
        try:
            video_clip = VideoFileClip(os.path.join(VIDEO_DIR, video))
            video_clips.append(video_clip)
        except Exception as e:
            continue
    
    final_clip = concatenate_videoclips(video_clips)

    save_path = os.path.join(OUTPUT_DIR, filename)
    final_clip.write_videofile(save_path, codec="libx264", fps=10)

if __name__ == "__main__":
    # image = "image_0.png"
    # audio = "audio_0_0.mp3"
    # text = "This is a sample video generated using the AI model."
    # generate_video(image, audio, text, "output.mp4")
    merge_video_clips("final_output.mp4")