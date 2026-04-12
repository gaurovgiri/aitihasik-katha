from story_gen import generate_story
from audio_gen import generate_audio, merge_audio_clips, get_audio_duration
from video_gen import create_video_clips, merge_video_clips, create_video_from_image
from subtitle_gen import generate_transcription, get_subtitle
from image_gen import generate_image
from datetime import timedelta
import os
from config import settings

def run_pipeline():
    story = generate_story()
    print("Story:\n", story)
    
    audio_filename = generate_audio(story, "story.mp3")
    total_audio_duration = get_audio_duration("story.mp3")
    transcription = generate_transcription(audio_filename)
    subtitles = get_subtitle(transcription)
    
    scenes = story.split(".")
    start_index = 0
    start_time = timedelta(seconds=0)
    for idx, scene in enumerate(scenes):
        image_path = generate_image(scene, story, f"image_{idx}.png")
        
        try:
            scene_last_subtitle = subtitles[start_index + len(scene.split())]
            end_time = timedelta(seconds=scene_last_subtitle[0][1])
        except IndexError:
            scene_last_subtitle = subtitles[-1]
            end_time = total_audio_duration
        
        duration = (end_time - start_time).total_seconds()
    
        start_time = end_time
        start_index = len(scene.split())
        
        create_video_from_image(image_path, duration, f"video_image_clip_{idx}.mp4")
        
    final_video = merge_video_clips("final_video.mp4", voice_over=audio_filename, subtitles=subtitles)
    print(f"The video is ready at {os.path.join(settings.VIDEO_PATH, final_video)}")

if __name__ == "__main__":
    run_pipeline()