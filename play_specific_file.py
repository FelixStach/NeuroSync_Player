# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

import sys
import os
import pygame
import warnings
from threading import Thread
import requests
from livelink.animations.default_animation import default_animation_loop, stop_default_animation
from livelink.connect.livelink_init import create_socket_connection, initialize_py_face
from livelink.animations.animation_loader import load_animation
from utils.generated_runners import run_audio_animation
from utils.emote_sender.send_emote import EmoteConnect

warnings.filterwarnings(
    "ignore",
    message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work"
)

ENABLE_EMOTE_CALLS = False

# ------------------ Script Functions ------------------ #
def print_usage():
    print("Usage:")
    print(" <shapes.csv> <audio.wav>")
    print("Arguments:")
    print("  <shapes.csv>   Path to the facial animation CSV file")
    print("  <audio.wav>    Path to the audio file")
    sys.exit(1)


def main(shapes_path: str, audio_path: str):
    print("Using provided file paths:")
    print(f"  Shapes path: {shapes_path}")
    print(f"  Audio path:  {audio_path}")

    # Load facial animation data
    try:
        generated_facial_data = load_animation(shapes_path)
    except Exception as e:
        print("Error loading facial data:", e)
        return

    if ENABLE_EMOTE_CALLS:
        EmoteConnect.send_emote("startspeaking")

    try:
        run_audio_animation(audio_path, generated_facial_data, py_face, socket_connection, default_animation_thread)
    except Exception as e:
        print("Error running audio animation:", e)
    finally:
        if ENABLE_EMOTE_CALLS:
            EmoteConnect.send_emote("stopspeaking")


# ------------------ Script Entry Point ------------------ #
if __name__ == '__main__':

    # Argument validation
    if len(sys.argv) != 3:
        print("[ERROR] Invalid number of arguments.")
        print_usage()

    shapes_path = sys.argv[1]
    audio_path = sys.argv[2]

    if not shapes_path.lower().endswith(".csv") or not audio_path.lower().endswith(".wav"):
        print("[ERROR] Invalid file types.")
        print_usage()

    if not os.path.isfile(shapes_path):
        print(f"[ERROR] Shapes file not found: {shapes_path}")
        sys.exit(1)

    if not os.path.isfile(audio_path):
        print(f"[ERROR] Audio file not found: {audio_path}")
        sys.exit(1)

    # Initialize LiveLink
    py_face = initialize_py_face()
    socket_connection = create_socket_connection()
    default_animation_thread = Thread(target=default_animation_loop, args=(py_face,))
    default_animation_thread.start()

    try:
        main(shapes_path, audio_path)
    finally:
        stop_default_animation.set()
        if default_animation_thread:
            default_animation_thread.join()
        pygame.quit()
        socket_connection.close()
