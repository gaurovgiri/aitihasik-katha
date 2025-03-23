from story_gen import generate_story
from audio_gen import generate_audio, merge_audio_clips
from video_gen import generate_video, merge_video_clips
from image_gen import generate_image
from helper import is_stop_word, split_sentences

def run_pipeline():
    story = generate_story()
    print("Story:\n", story)
    generate_audio(story, "story.mp3")

    sentences = story.split(".")
    segmented_stories = [". ".join(sentences[i: i+2]).strip() for i in range(0, len(sentences), 2)]

    for idx, segment in enumerate(segmented_stories):
        image = generate_image(segment, f"image_{idx}.png")
        overlay_texts = split_sentences(segment)

        for sub_idx, groups in enumerate(overlay_texts):
            try:
                audio = generate_audio(groups, f"audio_{idx}_{sub_idx}.mp3")
                video = generate_video(f"image_{idx}.png", f"audio_{idx}_{sub_idx}.mp3", groups, f"video_{idx}_{sub_idx}.mp4")
            except:
                continue
            
    merge_audio_clips("merged_story.mp3")
    merge_video_clips("final_output.mp4", voice_over="story.mp3")

if __name__ == "__main__":
    run_pipeline()