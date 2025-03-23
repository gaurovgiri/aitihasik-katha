import gtts
from gtts.tokenizer import pre_processors
from story_gen import generate_story
import os
from config import AUDIO_DIR
from moviepy import AudioFileClip, concatenate_audioclips

def merge_audio_clips(filename):
    """Merge multiple audio clips into a single audio clip."""
    audios = os.listdir(AUDIO_DIR)
    audios.remove("story.mp3")

    audios = sorted(audios, key=lambda v: tuple(map(int, v.replace(".mp3", "").split("_")[1:])))
    audio_clips = []
    for audio in audios:
        try:
            audio_clip = AudioFileClip(os.path.join(AUDIO_DIR, audio))
            audio_clips.append(audio_clip)
        except Exception as e:
            continue
    
    final_audio = concatenate_audioclips(audio_clips)
    save_path = os.path.join(AUDIO_DIR, filename)
    final_audio.write_audiofile(save_path)


def generate_audio(text, filename):
    """Generate an audio file from the given text."""
    tts = gtts.gTTS(text, slow=False,
                    lang="hi"
                )

    save_path = os.path.join(AUDIO_DIR, filename)
    tts.save(save_path)

if __name__ == "__main__":
    # text = generate_story()
    # generate_audio("hello my name is. Gaurav Giri.", "test.mp3")
    merge_audio_clips("merged_story.mp3")