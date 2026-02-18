# Voxpipe Roadmap

This file outlines where the project is going and what features are planned.

## Current Status

Basic infrastructure is working:
- State management (IDLE, LISTENING, SPEAKING)
- Cancellation system (prevents overlap)
- Text-to-speech output
- Audio capture

## Planned Features

### Phase 1: Voice Activation
- [ ] Detect when user starts speaking
- [ ] Automatically switch from LISTENING to SPEAKING
- [ ] Detect when user stops speaking
- [ ] Configurable volume threshold

### Phase 2: Speech Recognition
- [ ] Convert captured audio to text
- [ ] Use a speech-to-text library
- [ ] Handle different audio formats

### Phase 3: AI Integration
- [ ] Connect to LLM or AI service
- [ ] Generate responses from transcribed text
- [ ] Make responses sound natural

### Phase 4: Conversation Flow
- [ ] Remember context between exchanges
- [ ] Handle interruptions gracefully
- [ ] Add wake word detection

## Priorities

The most important thing is making sure listening and speaking never overlap. Every feature must respect the cancellation system we built.

## Contributing

This is a learning project. Feel free to fork and try different approaches.
