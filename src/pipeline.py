from story_gen import generate_story
from audio_gen import generate_audio, get_audio_duration
from video_gen import merge_video_clips, create_video_from_image
from subtitle_gen import generate_transcription, get_subtitle
from image_gen import generate_image
import os
import re
from config import settings

def run_pipeline():
    story = generate_story()
    print("Story:\n", story)
    
    audio_filename = generate_audio(story, "story.mp3")
    total_audio_duration = get_audio_duration("story.mp3")
    transcription = generate_transcription(audio_filename)
    subtitles = get_subtitle(transcription)
    
    scenes = [s.strip() for s in re.split(r"[.!?]+", story) if s.strip()]
    if not scenes:
        scenes = [story.strip()]

    total_audio_seconds = total_audio_duration.total_seconds()
    total_scene_words = max(1, sum(len(scene.split()) for scene in scenes))
    cumulative_words = 0
    start_seconds = 0.0
    generated_video_clips = []

    for idx, scene in enumerate(scenes):
        scene_words = max(1, len(scene.split()))
        cumulative_words += scene_words
        image_path = generate_image(scene, story, f"image_{idx}.png")

        if subtitles:
            subtitle_index = min(cumulative_words - 1, len(subtitles) - 1)
            end_seconds = float(subtitles[subtitle_index][0][1])
        else:
            progress = min(1.0, cumulative_words / total_scene_words)
            end_seconds = total_audio_seconds * progress

        if idx == len(scenes) - 1:
            end_seconds = max(end_seconds, total_audio_seconds)

        # Guard against non-monotonic or tiny durations from timing drift.
        end_seconds = max(end_seconds, start_seconds + 0.6)
        duration = end_seconds - start_seconds
        start_seconds = end_seconds

        video_filename = f"video_image_clip_{idx}.mp4"
        create_video_from_image(image_path, duration, video_filename)
        generated_video_clips.append(video_filename)

    final_video = merge_video_clips(
        "final_video.mp4",
        voice_over=audio_filename,
        subtitles=subtitles,
        clip_filenames=generated_video_clips,
    )
    print(f"The video is ready at {os.path.join(settings.OUTPUT_PATH, final_video)}")

if __name__ == "__main__":
    run_pipeline()