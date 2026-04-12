from google.cloud import texttospeech
import os
from config import settings
from moviepy import AudioFileClip, concatenate_audioclips
from datetime import timedelta
import random


VOICE_PROMPTS = [
    "Clear, engaging storytelling voice with a fast-medium pace, confident tone, crisp pronunciation, and strong emphasis on hook words for high retention.",

    "Cinematic documentary-style voice with a medium-fast pace, authoritative tone, sharp articulation, and impactful emphasis on key moments.",

    "High-energy viral shorts voice with fast-paced delivery, dynamic rhythm, strong hooks, and punchy emphasis to удерж attention instantly.",

    "Clear educational voice with a medium-fast pace, confident tone, precise pronunciation, and structured emphasis for quick understanding.",

    "Dramatic storytelling voice with a medium-fast pace, mysterious tone, cinematic flow, and suspense-driven emphasis.",

    "Smooth but engaging narration voice with a medium-fast pace, warm tone, and clear articulation designed for continuous attention.",

    "Epic cinematic voice with a medium pace leaning fast, powerful tone, strong dramatic emphasis, and trailer-like intensity.",

    "Neutral professional voice with a medium-fast pace, clear articulation, and factual delivery suitable for concise historical explanations.",

    "Hook-optimized voice with fast opening delivery, sharp clarity, and strong emphasis on curiosity-driven words to grab attention immediately.",

    "Natural creator-style voice with a fast-medium pace, expressive tone, smooth flow, and engaging emphasis for viral storytelling content."
]


client = texttospeech.TextToSpeechClient()

def merge_audio_clips(filename):
    """Merge multiple audio clips into a single audio clip."""
    audios = os.listdir(settings.AUDIO_PATH)
    audios.remove("story.mp3")

    audios = sorted(audios, key=lambda v: tuple(map(int, v.replace(".mp3", "").split("_")[1:])))
    audio_clips = []
    for audio in audios:
        try:
            audio_clip = AudioFileClip(os.path.join(settings.AUDIO_PATH, audio))
            audio_clips.append(audio_clip)
        except Exception as e:
            continue
    
    final_audio = concatenate_audioclips(audio_clips)
    save_path = os.path.join(settings.AUDIO_PATH, filename)
    final_audio.write_audiofile(save_path)

def get_audio_duration(filename):
    audio = os.path.join(settings.AUDIO_PATH, filename)
    audio_clip = AudioFileClip(audio)
    return timedelta(seconds=audio_clip.duration)


def generate_audio(text, filename):
    """Generate an audio file from the given text."""
    voice_prompt = random.choice(VOICE_PROMPTS)
    print(f"Using following voice prompt: {voice_prompt}")
    synthesis_input = texttospeech.SynthesisInput(text=text, prompt=voice_prompt)

    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='Charon',
        model_name=settings.AUDIO_MODEL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    output_filepath = os.path.join(settings.AUDIO_PATH, filename)

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file: {output_filepath}")
    return filename

if __name__ == "__main__":
    # generate_audio('hello, this is a test audio for the aitihasik katha', 'audio.mp3')
    print(get_audio_duration("test.mp3"))