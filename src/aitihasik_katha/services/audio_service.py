import os
import random
from datetime import timedelta

from google.cloud import texttospeech
from moviepy import AudioFileClip, concatenate_audioclips

from ..core.settings import settings


VOICE_PROMPTS = [
    "Clear, engaging storytelling voice with a fast-medium pace, confident tone, crisp pronunciation, and strong emphasis on hook words for high retention.",
    "Cinematic documentary-style voice with a medium-fast pace, authoritative tone, sharp articulation, and impactful emphasis on key moments.",
    "High-energy viral shorts voice with fast-paced delivery, dynamic rhythm, strong hooks, and punchy emphasis to retain attention instantly.",
    "Clear educational voice with a medium-fast pace, confident tone, precise pronunciation, and structured emphasis for quick understanding.",
    "Dramatic storytelling voice with a medium-fast pace, mysterious tone, cinematic flow, and suspense-driven emphasis.",
    "Smooth but engaging narration voice with a medium-fast pace, warm tone, and clear articulation designed for continuous attention.",
    "Epic cinematic voice with a medium pace leaning fast, powerful tone, strong dramatic emphasis, and trailer-like intensity.",
    "Neutral professional voice with a medium-fast pace, clear articulation, and factual delivery suitable for concise historical explanations.",
    "Hook-optimized voice with fast opening delivery, sharp clarity, and strong emphasis on curiosity-driven words to grab attention immediately.",
    "Natural creator-style voice with a fast-medium pace, expressive tone, smooth flow, and engaging emphasis for viral storytelling content.",
]


client = texttospeech.TextToSpeechClient()


def get_audio_duration(audio_filepath: str) -> timedelta:
    audio_clip = AudioFileClip(audio_filepath)
    duration = timedelta(seconds=audio_clip.duration)
    audio_clip.close()
    return duration


def generate_audio(text: str, output_path: str) -> str:
    """Generate an MP3 audio file from plain text narration."""
    voice_prompt = random.choice(VOICE_PROMPTS)
    print(f"Using following voice prompt: {voice_prompt}")
    synthesis_input = texttospeech.SynthesisInput(text=text, prompt=voice_prompt)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="Charon",
        model_name=settings.AUDIO_MODEL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file: {output_path}")

    return output_path
