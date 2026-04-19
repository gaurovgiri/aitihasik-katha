import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from ..core.settings import settings
from ..utils.gcs import delete_file_from_gcs, upload_file_to_gcs


client = SpeechClient()


def _generate_transcription(audio_file: str) -> cloud_speech.RecognizeResponse:
    """Transcribe a GCS audio file URI with word-level time offsets."""
    features = cloud_speech.RecognitionFeatures(
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
        features=features,
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=audio_file)
    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{settings.PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    operation = client.batch_recognize(request=request)
    response = operation.result(timeout=120)
    return response.results[audio_file].transcript


def generate_transcription(audio_file: str):
    audio_file_path = os.path.join(settings.AUDIO_PATH, audio_file)
    bucket_file_path = upload_file_to_gcs(settings.BUCKET, audio_file_path, audio_file, return_public=False)
    response = _generate_transcription(bucket_file_path)
    delete_file_from_gcs(bucket_file_path)
    return response


def get_subtitle(speech_to_text_response) -> list[tuple[tuple[float, float], str]]:
    subs = []
    for result in speech_to_text_response.results:
        for words in result.alternatives[0].words:
            start_time = words.start_offset.total_seconds()
            end_time = words.end_offset.total_seconds()
            subs.append(((start_time, end_time), words.word))
    return subs
