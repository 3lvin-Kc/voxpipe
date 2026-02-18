# Voxpipe - Voice Assistant Framework

Voxpipe is a lightweight framework for building voice assistants. It handles the core problem: making sure listening and speaking never overlap, and everything stops cleanly when needed.

## What It Does

The app runs in a continuous loop with two main states:

- **Listening**: Opens your microphone and captures audio
- **Speaking**: Uses text-to-speech to talk back

In demo mode, it switches between these states every 5 seconds so you can see how it works.

## Quick Start

```cmd
.venv\Scripts\python.exe main.py
```

Press Ctrl+C to stop.

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

When switching states, the controller automatically cancels any ongoing operation. This prevents audio overlap and ensures clean transitions.

## Project Files

| File | What It Is |
|------|------------|
| main.py | Entry point - runs the voice loop |
| controller.py | State management - controls when to listen/speak |
| requirements.txt | Python dependencies |

## Features Right Now

- Real-time audio volume monitoring
- Text-to-speech output
- Automatic state switching (demo mode)
- Clean cancellation when states change

## What's Coming

Check ROADMAP.md for planned features and where the project is heading.
