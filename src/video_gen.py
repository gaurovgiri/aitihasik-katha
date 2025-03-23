from moviepy import *
import os
from config import VIDEO_DIR, IMAGE_DIR, AUDIO_DIR, OUTPUT_DIR
from helper import is_stop_word

def format_text(text):
    text = text.strip().replace("\n", " ")
    words = text.split()
    formatted_text = ""
    while len(words) > 5:
        first_part = " ".join(words[:5])
        formatted_text += f" {first_part} \n"
        words = words[5:]
    formatted_text += f" {' '.join(words)} "
    return formatted_text


def generate_video(image, audio, text, filename):
    audio_path = os.path.join(AUDIO_DIR, audio)
    image_path = os.path.join(IMAGE_DIR, image)

    audio_clip = AudioFileClip(audio_path)
    # audio_clip = audio_clip.with_speed_scaled(1.05)

    image_clip = ImageClip(image_path)
    
    formatted_text = format_text(text)
    text_clip = TextClip(font="Impact", text=formatted_text, font_size=40, color='White', stroke_color='Black', stroke_width=2, text_align="center")
    text_clip = text_clip.with_position(("center", "center"))


    if any(is_stop_word(word) for word in formatted_text.split()):
        image_clip = image_clip.with_duration(audio_clip.duration + 0.125)
        text_clip = text_clip.with_duration(audio_clip.duration + 0.125)

    else:
        image_clip = image_clip.with_duration(audio_clip.duration - 0.125)
        text_clip = text_clip.with_duration(audio_clip.duration - 0.125)

    video = CompositeVideoClip([image_clip, text_clip])
    
    

    save_path = os.path.join(VIDEO_DIR, filename)
    video.write_videofile(save_path, codec="libx264", fps=10)

def merge_video_clips(filename, voice_over=None, background_music=None):
    videos = os.listdir(VIDEO_DIR)
    videos = sorted(videos, key=lambda v: tuple(map(int, v.replace(".mp4", "").split("_")[1:])))

    merged_audio_clip = AudioFileClip(os.path.join(AUDIO_DIR, "merged_story.mp3"))
    story_audio_clip = AudioFileClip(os.path.join(AUDIO_DIR, "story.mp3"))

    duration_diff = merged_audio_clip.duration - story_audio_clip.duration
    clipping_duration = duration_diff / len(videos)


    video_clips = []
    for video in videos:
        try:
            video_clip = VideoFileClip(os.path.join(VIDEO_DIR, video))
            video_clip = video_clip.subclipped(0, -clipping_duration)
            video_clips.append(video_clip)
        except Exception as e:
            continue

    final_clip = concatenate_videoclips(video_clips)

    if voice_over:
        voice_clip = AudioFileClip(os.path.join(AUDIO_DIR, voice_over))
        final_clip = final_clip.with_audio(voice_clip)
    if background_music:
        bgm_clip = AudioFileClip(os.path.join(AUDIO_DIR, background_music))
        final_clip = final_clip.with_audio(bgm_clip)

    save_path = os.path.join(OUTPUT_DIR, filename)
    final_clip.write_videofile(save_path, codec="libx264", fps=10)

if __name__ == "__main__":
    merge_video_clips("final_output.mp4", "story.mp3")