import os
import re

from .core.settings import ensure_directories, settings
from .services.audio_service import generate_audio, get_audio_duration
from .services.image_service import generate_image
from .services.story_service import generate_story
from .services.subtitle_service import generate_transcription, get_subtitle
from .services.caption_service import generate_caption
from .services.video_service import create_video_from_image, merge_video_clips
from .utils.gcs import upload_file_to_gcs
from .services.instagram_service import instagram
import uuid

def run_pipeline(topic: str | None = None) -> str | None:
    current_run_uuid = uuid.uuid4()
    ensure_directories(str(current_run_uuid))

    story = generate_story(topic=topic)
    print("Story:\n", story)

    audio_output_filepath = os.path.join(settings.RUNS_PATH, str(current_run_uuid), settings.AUDIO_PATH, "story.mp3")

    audio_filename = generate_audio(story, audio_output_filepath)
    total_audio_duration = get_audio_duration(audio_filename)
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
        image_output_filepath = os.path.join(settings.RUNS_PATH, str(current_run_uuid), settings.IMAGE_PATH, f"image_{idx}.png")
        image_path = generate_image(scene, story, image_output_filepath)

        if subtitles:
            subtitle_index = min(cumulative_words - 1, len(subtitles) - 1)
            end_seconds = float(subtitles[subtitle_index][0][1])
        else:
            progress = min(1.0, cumulative_words / total_scene_words)
            end_seconds = total_audio_seconds * progress

        if idx == len(scenes) - 1:
            end_seconds = max(end_seconds, total_audio_seconds)

        end_seconds = max(end_seconds, start_seconds + 0.6)
        duration = end_seconds - start_seconds
        start_seconds = end_seconds

        imageclip_output_filepath = os.path.join(settings.RUNS_PATH, str(current_run_uuid), settings.VIDEO_PATH, f"video_image_clip_{idx}.mp4")
        
        imageclip_path =  create_video_from_image(image_path, duration, imageclip_output_filepath)
        generated_video_clips.append(imageclip_path)

    final_video_output_filepath = os.path.join(settings.RUNS_PATH, str(current_run_uuid), settings.OUTPUT_PATH, "final_video.mp4")
    final_video_path = merge_video_clips(
        final_video_output_filepath,
        voice_over=audio_filename,
        subtitles=subtitles,
        clip_filenames=generated_video_clips,
    )

    if final_video_path:
        print(f"The video is ready at {final_video_path}")
        media_uri = upload_file_to_gcs(settings.BUCKET, final_video_path, final_video_path)
        print(f"The video is uploaded to {media_uri}")
        print(f"Generating a caption for this video")
        caption = generate_caption(story)
        print(f"Uploading to instagram!")
        instagram.upload_media(media_uri, 
                               caption=caption, 
                               media_type="REELS")
        print(f"Upload complete to instagram!")




if __name__ == "__main__":
    run_pipeline()
