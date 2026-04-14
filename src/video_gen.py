from moviepy import *
import os
import re
import math
from config import settings
from google import genai
from google.genai.types import GenerateVideosConfig,GenerateVideosSource
from moviepy.video.tools.subtitles import file_to_subtitles
import time

client = genai.Client()
config = GenerateVideosConfig(
    aspect_ratio="9:16",
    number_of_videos=1,
    duration_seconds=8,
    person_generation="allow_all",
    resolution="720p",
)

def format_text(text):
    text = text.strip().replace("\n", " ")
    words = text.split()
    formatted_text = ""
    while len(words) > 5:
        first_part = " ".join(words[:5])
        formatted_text += f" {first_part} \n"
        words = words[5:]
    formatted_text += f" {' '.join(words)} "
    return formatted_text


def _build_video_prompt(current_scene, full_story):
    return f"""
            Create a cinematic, fun and educational video.

            Full story context (for narrative understanding only):
            {full_story}

            Current scene (focus only on this moment):
            {current_scene}

            Instructions:
            - Maintain strict consistency in characters, clothing, environment, and style
            - Characters must look the same across all clips
            - Use cinematic camera movement (slow pan, slight zoom, or tracking)
            - Include natural motion (walking, gestures, environment movement like wind, dust, etc.)
            - Keep pacing smooth and visually clear

            Style:
            - Cinematic realism
            - Warm, engaging color tones
            - Dramatic but fun and educational feel
            - High detail and depth

            Restrictions:
            - No modern elements
            - No text, captions, or watermark

            Output:
            A smooth, visually consistent 8-second cinematic video clip.
        """

def generate_video(text, full_story, filename):
    """Generate a video for the given scene text and save it to disk."""
    source = GenerateVideosSource(prompt=_build_video_prompt(text, full_story))
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        source=source,
        config=config,
    )

    while not operation.done:
        print("Video has not been generated. Check again in 10 seconds...")
        time.sleep(10)
        operation = client.operations.get(operation)

    if not operation.response or not operation.response.generated_videos:
        print("No videos were generated!")
        return

    generated_video = operation.response.generated_videos[0]
    output_path = os.path.join(settings.VIDEO_PATH, filename)

    if generated_video.video:
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_path)
        print(f"Generated video saved to {output_path}")
    else:
        print("Error occurred while generating video")

def create_video_clips(image, audio, text, filename):
    audio_path = os.path.join(settings.AUDIO_PATH, audio)
    image_path = os.path.join(settings.IMAGE_PATH, image)

    audio_clip = AudioFileClip(audio_path)
    # audio_clip = audio_clip.with_speed_scaled(1.05)

    image_clip = ImageClip(image_path)
    
    formatted_text = format_text(text)
    text_clip = TextClip(text=formatted_text, font_size=40, color='White', stroke_color='Black', stroke_width=2, text_align="center")
    text_clip = text_clip.with_position(("center", "center"))

    video = CompositeVideoClip([image_clip, text_clip])

    save_path = os.path.join(settings.VIDEO_PATH, filename)
    video.write_videofile(save_path, codec="libx264", fps=24)

def create_video_from_image(image_filename, duration, filename):
    image_path = os.path.join(settings.IMAGE_PATH, image_filename)
    safe_duration = max(0.6, float(duration))
    image_clip = ImageClip(image_path)
    image_clip = image_clip.with_duration(safe_duration)

    def _ease_in_zoom_scale(t):
        zoom_target = 1.18
        progress = min(1.0, max(0.0, t / safe_duration))
        eased_progress = 0.65 * progress + 0.35 * (1.0 - (1.0 - progress) * (1.0 - progress))
        return 1.0 + (zoom_target - 1.0) * eased_progress

    zoomed_image = image_clip.with_effects([vfx.Resize(_ease_in_zoom_scale)]).with_position(("center", "center"))
    video = CompositeVideoClip([zoomed_image], size=(image_clip.w, image_clip.h))
    save_path = os.path.join(settings.VIDEO_PATH, filename)
    video.write_videofile(save_path, codec="libx264", fps=24)
    video.close()
    zoomed_image.close()
    image_clip.close()
    return filename


def _build_reels_caption_clip(text, start_time, end_time, video_w, video_h):
    """Create a glowing subtitle clip with a one-time intro pop animation."""
    duration = max(0.1, float(end_time) - float(start_time))
    caption_text = format_text(text).upper()
    caption_font = "data/fonts/KOMIKAX_.ttf"

    font_size = max(52, int(video_w * 0.082))
    max_text_width = int(video_w * 0.9)
    caption_box_h = int(video_h * 0.24)

    text_kwargs = dict(
        text=caption_text,
        method="caption",
        size=(max_text_width, caption_box_h),
        font=caption_font,
        margin=(20, 20),
        font_size=font_size,
        text_align="center",
        horizontal_align="center",
        vertical_align="center",
        transparent=True,
        interline=8,
        duration=duration,
    )

    shadow = TextClip(
        **text_kwargs,
        color="black",
        stroke_color="black",
        stroke_width=8,
    ).with_opacity(0.28).with_position((2, 3))

    glow_halo = TextClip(
        **text_kwargs,
        color="#fff8d6",
        stroke_color="#fff8d6",
        stroke_width=16,
    ).with_opacity(0.18)

    glow_outer = TextClip(
        **text_kwargs,
        color="#fff7b0",
        stroke_color="#fff7b0",
        stroke_width=12,
    ).with_opacity(0.30)

    glow_inner = TextClip(
        **text_kwargs,
        color="#fffdf2",
        stroke_color="#ffffff",
        stroke_width=9,
    ).with_opacity(0.22)

    main = TextClip(
        **text_kwargs,
        color="#ffffff",
        stroke_color="#0b1020",
        stroke_width=4,
    )

    def _bump_scale(t):
        intro_duration = 0.22
        settled_scale = 1.06
        if t >= intro_duration:
            return settled_scale

        # Fast punch-in with one quick overshoot, then hold steady.
        p = t / intro_duration
        base_lift = (settled_scale - 1.0) * p
        overshoot = 0.10 * math.sin(math.pi * p) * math.exp(-3.8 * p)
        return 1.0 + base_lift + overshoot

    pad = max(24, int(font_size * 0.9))
    layer_w = max(shadow.w, glow_halo.w, glow_outer.w, glow_inner.w, main.w)
    layer_h = max(shadow.h, glow_halo.h, glow_outer.h, glow_inner.h, main.h)
    canvas_size = (layer_w + 2 * pad, layer_h + 2 * pad)
    animated_caption = CompositeVideoClip(
        [
            shadow.with_position(("center", "center")),
            glow_halo.with_position(("center", "center")),
            glow_outer.with_position(("center", "center")),
            glow_inner.with_position(("center", "center")),
            main.with_position(("center", "center")),
        ],
        size=canvas_size,
        bg_color=None,
    )
    animated_caption = animated_caption.with_effects([vfx.Resize(_bump_scale)])

    max_scale = 1.16
    reserved_h = int(animated_caption.h * max_scale)
    target_center_y = int(video_h * 0.62)  # slightly below vertical center
    caption_y = max(0, target_center_y - (reserved_h // 2))

    full_frame_caption = CompositeVideoClip(
        [animated_caption.with_position(("center", caption_y))],
        size=(video_w, video_h),
        bg_color=None,
    )
    return full_frame_caption.with_start(start_time).with_end(end_time)

    
def merge_video_clips(filename=None, voice_over=None, subtitles=None, background_music=None, clip_filenames=None):
    """Merge all generated video clips, optionally apply audio, and write the final output file."""
    output_filename = filename or "final_output.mp4"
    if clip_filenames:
        videos = [v for v in clip_filenames if v.lower().endswith(".mp4")]
    else:
        videos = [v for v in os.listdir(settings.VIDEO_PATH) if v.lower().endswith(".mp4")]

    def _video_sort_key(video_name):
        stem = os.path.splitext(video_name)[0]
        match = re.search(r"(\d+)$", stem)
        index = int(match.group(1)) if match else float("inf")
        return (index, stem)

    videos = sorted(videos, key=_video_sort_key)

    if not videos:
        print(f"No video clips found in {settings.VIDEO_PATH}. Skipping merge.")
        return None

    video_clips = []
    for video in videos:
        try:
            video_clip = VideoFileClip(os.path.join(settings.VIDEO_PATH, video))
            video_clips.append(video_clip)
        except (OSError, ValueError) as e:
            print(f"Error occurred while loading clip '{video}': {e}")
            continue

    if not video_clips:
        print("No valid video clips could be loaded. Skipping merge.")
        return None

    final_clip = concatenate_videoclips(video_clips)
    voice_clip = None
    bgm_clip = None

    if voice_over:
        voice_clip = AudioFileClip(os.path.join(settings.AUDIO_PATH, voice_over))
        final_clip = final_clip.with_audio(voice_clip)
    if subtitles:
        subtitle_items = file_to_subtitles(subtitles) if isinstance(subtitles, (str, os.PathLike)) else subtitles
        subtitle_overlays = [
            _build_reels_caption_clip(text, start, end, final_clip.w, final_clip.h)
            for (start, end), text in subtitle_items
        ]
        final_clip = CompositeVideoClip([final_clip, *subtitle_overlays])
    if background_music:
        bgm_clip = AudioFileClip(os.path.join(settings.AUDIO_PATH, background_music))
        final_clip = final_clip.with_audio(bgm_clip)

    save_path = os.path.join(settings.OUTPUT_PATH, output_filename)
    final_clip.write_videofile(save_path, codec="libx264", fps=24)
    final_clip.close()
    for clip in video_clips:
        clip.close()
    if voice_clip:
        voice_clip.close()
    if bgm_clip:
        bgm_clip.close()
    return output_filename

if __name__ == "__main__":
    demo_subtitles = [
    ((0.0, 1.0), 'This'),
    ((1.0, 2.0), 'is'),
    ((2.0, 3.0), 'the'),
    ((3.0, 4.0), 'beginning'),
    
    ((4.0, 5.2), 'of'),
    ((5.2, 6.4), 'a'),
    ((6.4, 7.6), 'story'),
    ((7.6, 9.0), 'that'),
    
    ((9.0, 10.0), 'slowly'),
    ((10.0, 11.0), 'unfolds'),
    ((11.0, 12.0), 'revealing'),
    
    ((12.0, 13.0), 'moments'),
    ((13.0, 14.0), 'of'),
    ((14.0, 15.0), 'tension'),
    ((15.0, 16.0), 'and')
    ]
    merge_video_clips("final_output.mp4", "story.mp3", demo_subtitles)