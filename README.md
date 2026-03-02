# Voxpipe - Voice Control Infrastructure

Voxpipe is infrastructure for building voice interactions that feel normal. It solves the core problem: **who is allowed to talk right now?**

## The Problem We Solve

Current voice tools break when humans behave normally:
- User interrupts mid-sentence
- User and app talk at the same time
- App doesn't stop talking when user speaks
- Audio overlaps, system gets confused

**This project is NOT a voice assistant or chatbot. It's the rules and control layer that other voice features run on.**

## What It Does

The app runs in a continuous loop with two main states:

- **Listening**: Opens your microphone and captures audio
- **Speaking**: Uses text-to-speech to talk back

## Quick Start

```cmd
.venv\Scripts\python.exe main.py
```

Press Ctrl+C to stop. Say something while the app is speaking to test interruption.

## Requirements

- Python 3.8 or newer
- sounddevice
- numpy
- pyttsx3

## Installing

```bash
pip install -r requirements.txt
```

The virtual environment already has everything you need.

## How It Works

The system has three states:

| State | What Happens |
|-------|-------------|
| IDLE | Nothing - waiting around |
| LISTENING | Microphone is open, capturing sound |
| SPEAKING | TTS is talking |

### Interruption Handler

When user speaks while app is SPEAKING:
1. Volume threshold detected in callback
2. Immediately cancel TTS (via CancelToken)
3. Switch to LISTENING state

The audio stream stays active during SPEAKING to detect interruptions.

### State Transitions

When switching states, the controller automatically cancels any ongoing operation. This prevents audio overlap and ensures clean transitions.

## Project Files

| File | What It Is |
|------|------------|
| main.py | Entry point - runs the voice loop with interruption handler |
| controller.py | State management - controls when to listen/speak |
| requirements.txt | Python dependencies |

## Features Right Now

- Real-time audio volume monitoring
- Text-to-speech output
- **Interruption Handler** - user can interrupt while app is speaking
- Automatic state switching (demo mode)
- Clean cancellation when states change
- Audio stream active during SPEAKING to detect interruptions

## Configuration

In `main.py`, adjust the volume threshold:

```python
VOLUME_THRESHOLD = 2.0  # Increase if too sensitive, decrease if not detecting speech
```

## What's Coming

Check ROADMAP.md for planned features and where the project is heading.
