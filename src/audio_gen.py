import gtts
from gtts.tokenizer import pre_processors
from story_gen import generate_story
import os
from config import AUDIO_DIR

def generate_audio(text, filename):
    """Generate an audio file from the given text."""
    tts = gtts.gTTS(text, slow=False, 
                pre_processor_funcs=[
                    pre_processors.tone_marks,
                    pre_processors.abbreviations,
                    pre_processors.word_sub,
                    # pre_processors.end_of_line
                    ],
                    lang="hi"
                )

    save_path = os.path.join(AUDIO_DIR, filename)
    tts.save(save_path)

if __name__ == "__main__":
    # text = generate_story()
    generate_audio("hello my name is.", "story.mp3")