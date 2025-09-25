# Felix' NeuroSync Player Fork

This project is forked from https://github.com/AnimaVR/NeuroSync_Player, which was archived by the owner on Jul 14, 2025.
This fork includes minor additions:
- script to send a single CSV shape file to UE5 (play_specific_file.py)
- requirements.txt now includes pyinstaller
- requirements.txt now names an older version of numpy that works well with PyInstaller
- provides batch script for running PyInstaller
- to avoid shipping the required default animation seperately, it is donwloaded (currently every time the program runs!)
- icon for the executable


# NeuroSync Player

## 29/03/2025 Update to model.pth and model.py in api's

- Increased accuracy (timing and overall face shows more natural movement overall, brows, squint, cheeks + mouth shapes)
- More smoothness during playback (flappy mouth be gone in most cases, even when speaking quickly)
- Works better with more voices and styles of speaking.
- This preview of the new model is a modest increase in capability that requires both model.pth and model.py to be replaced with the new versions.

[Download the model from Hugging Face](https://huggingface.co/AnimaVR/NEUROSYNC_Audio_To_Face_Blendshape)

## Overview

The **NeuroSync Player** allows for real-time streaming of facial blendshapes into Unreal Engine 5 using LiveLink - enabling facial animation from audio input.

### Features:
- Real-time facial animation
- Integration with Unreal Engine 5 via LiveLink
- Supports blendshapes generated from audio inputs

## NeuroSync Model

To generate facial blendshapes from audio, you'll need the **NeuroSync audio-to-face blendshape transformer model**. You can:

-To host the model locally, you can set up the [NeuroSync Local API](https://github.com/AnimaVR/NeuroSync_Local_API).
- [Download the model from Hugging Face](https://huggingface.co/AnimaVR/NEUROSYNC_Audio_To_Face_Blendshape)

### Switching Between Local and Non-Local API

The player can connect to either the **local API** or the **alpha API** depending on your needs. To switch between the two, simply change the boolean value in the `utils/neurosync/neurosync_api_connect.py` file:

### **12/03/2025 Local Real-Time API Toy**

[Realtime AI endpoint server](https://github.com/AnimaVR/NeuroSync_Real-Time_API) that combines tts and neurosync generations available.

Includes code for various helpful AI endpoints (stt, tts, embedding, vision) to use with the player, or your own projects. Be mindful of licences for your use case.

**Demo Build**: [Download the demo build](https://drive.google.com/drive/folders/1q-CYauPqyWfvs8NamW4QuC1H1r02RYMQ?usp=sharing) to test NeuroSync with an Unreal Project (aka, free realistic AI companion when used with llm_to_face.py *wink* )

Talk to a NeuroSync prototype live on Twitch : [Visit Mai](https://www.twitch.tv/mai_anima_ai)

