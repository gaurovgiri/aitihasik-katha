from story_gen import generate_story
from audio_gen import generate_audio
from video_gen import generate_video, merge_video_clips
from image_gen import generate_image

def run_pipeline():
    story = generate_story()
    print("Story:\n", story)

    sentences = story.split(".")
    segmented_stories = [". ".join(sentences[i: i+2]) for i in range(0, len(sentences), 2)]

    for idx, segment in enumerate(segmented_stories):
        image = generate_image(segment, f"image_{idx}.png")
        words = segment.split(' ')
        group_size = 5
        group_of_five_words = [" ".join(words[i: i+group_size]) for i in range(0, len(words), group_size)]
        for sub_idx, groups in enumerate(group_of_five_words):
            audio = generate_audio(groups, f"audio_{idx}_{sub_idx}.mp3")
            video = generate_video(f"image_{idx}.png", f"audio_{idx}_{sub_idx}.mp3", groups, f"video_{idx}_{sub_idx}.mp4")

    merge_video_clips("data/output/final_output.mp4")

if __name__ == "__main__":
    run_pipeline()