# Voxpipe OpenClaw Integration

Give your Voxpipe voice assistant a brain.

## What This Does

Connects Voxpipe (voice I/O) to OpenClaw (AI agent) via open-engine (state persistence).

**Result:** A voice-enabled AI companion that remembers conversations.

```
User speaks → Voxpipe captures → OpenClaw processes → Voxpipe speaks response
                    ↓                        ↓
            Conversation state persisted via open-engine
```

## Quick Start

### 1. Start open-engine

```bash
cd open-engine/state-engine
cargo run -- serve --database voxpipe.db
```

### 2. Install Integration

```bash
cd integrations/openclaw
pip install -r requirements.txt
```

### 3. Run Voice Agent

```bash
python openclaw_voice_agent.py
```

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│ Voxpipe     │──────▶│ OpenClaw Bridge  │──────▶│ OpenClaw Agent  │
│ (Voice I/O) │      │ (State + Routing)│      │ (Doremon/AI)    │
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ open-engine      │
                    │ (Persistence)    │
                    └──────────────────┘
```

## Features

- ✅ **Persistent conversations** - Resume where you left off
- ✅ **No audio overlap** - Clean speaking/listening states
- ✅ **Interruption handling** - Talk over the AI, it listens
- ✅ **Context awareness** - AI remembers what you said

## Configuration

Edit `config.yaml`:

```yaml
openclaw:
  url: "http://127.0.0.1:3030"
  user_id: "your-user-id"
  agent_id: "doremon"

voxpipe:
  demo_mode: false
  listen_timeout: 5.0
  
session:
  auto_resume: true
  persist_history: true
```

## API

```python
from integrations.openclaw.controller import VoxpipeOpenClawController

controller = VoxpipeOpenClawController()
await controller.start()

# In your Voxpipe loop:
while True:
    transcript = voxpipe.listen()
    response = await controller.handle_speech(transcript)
    voxpipe.speak(response)
```

## Roadmap

- [ ] Full OpenClaw session integration
- [ ] Multi-agent support
- [ ] Voice cloning
- [ ] Web dashboard
- [ ] Cloud hosted option

## License

MIT
