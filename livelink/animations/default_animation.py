# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

import time
import socket
import pandas as pd
from threading import Event
import os
import requests

from livelink.connect.livelink_init import FaceBlendShape, UDP_IP, UDP_PORT
from livelink.animations.blending_anims import blend_animation_start_end
from livelink.animations.blending_anims import default_animation_state, blend_animation_start_end

# ==================== DEFAULT CSV CHECK & DOWNLOAD ====================

def ensure_default_csv():
    # Path to the existing livelink folder
    # If this script is inside livelink, use that folder directly
    base_dir = os.path.abspath(os.path.dirname(__file__))  # script directory

    # Check if 'animations' folder exists in this folder; if not, assume script is in a subfolder
    if not os.path.exists(os.path.join(base_dir, "animations")):
        # Go up one folder
        base_dir = os.path.abspath(os.path.join(base_dir, ".."))

    default_csv_path = os.path.join(base_dir, "animations", "default_anim", "default.csv")
    folder_path = os.path.dirname(default_csv_path)

    # Create folder structure if missing
    if not os.path.exists(folder_path):
        print(f"Creating missing directories: {folder_path}")
        os.makedirs(folder_path, exist_ok=True)

    # Download the CSV if it doesn't exist
    if not os.path.isfile(default_csv_path):
        default_csv_url = "https://raw.githubusercontent.com/AnimaVR/NeuroSync_Player/refs/heads/main/livelink/animations/default_anim/default.csv"
        print(f"Default CSV not found. Downloading from {default_csv_url}...")
        try:
            import requests
            response = requests.get(default_csv_url)
            response.raise_for_status()
            with open(default_csv_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded default CSV to {default_csv_path}")
        except requests.RequestException as e:
            print(f"Failed to download default CSV: {e}")
            raise SystemExit(1)
    else:
        print(f"Default CSV already exists: {default_csv_path}")

    return default_csv_path


# Ensure default CSV exists and get the path
ground_truth_path = ensure_default_csv()


# ==================== ANIMATION LOADING ====================

def load_animation(csv_path):
    data = pd.read_csv(csv_path)

    data = data.drop(columns=['Timecode', 'BlendshapeCount'])
    # zero'ing eyes so they match the generation position, do some eye control from Unreal or manually.
    cols_to_zero = [1, 2, 3, 4, 8, 9, 10, 11]
    cols_to_zero = [i for i in cols_to_zero if i < data.shape[1]] 
    data.iloc[:, cols_to_zero] = 0.0

    return data.values


# Load the default animation data
default_animation_data = load_animation(ground_truth_path)

# Create the blended default animation data
default_animation_data = blend_animation_start_end(default_animation_data, blend_frames=16)

# Event to signal stopping of the default animation loop
stop_default_animation = Event()


# ==================== DEFAULT ANIMATION LOOP ====================

def default_animation_loop(py_face):
    """
    Loops through the default animation and updates global index state.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((UDP_IP, UDP_PORT))
        while not stop_default_animation.is_set():
            for idx, frame in enumerate(default_animation_data):
                if stop_default_animation.is_set():
                    break
                # update shared state
                default_animation_state['current_index'] = idx

                for i, value in enumerate(frame):
                    py_face.set_blendshape(FaceBlendShape(i), float(value))
                try:
                    s.sendall(py_face.encode())
                except Exception as e:
                    print(f"Error in default animation sending: {e}")

                # maintain 60fps
                total_sleep = 1 / 60
                sleep_interval = 0.005
                while total_sleep > 0 and not stop_default_animation.is_set():
                    time.sleep(min(sleep_interval, total_sleep))
                    total_sleep -= sleep_interval
