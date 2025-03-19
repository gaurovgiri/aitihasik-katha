import gtts
from story_gen import generate_story
import os
from config import AUDIO_DIR

def generate_audio(text, filename):
    """Generate an audio file from the given text."""
    tts = gtts.gTTS(text, slow=False)

    save_path = os.path.join(AUDIO_DIR, filename)
    tts.save(save_path)

if __name__ == "__main__":
    # text = generate_story()
    generate_audio("", "data/audio/story.mp3")