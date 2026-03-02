hello (here's how i see this project)

building this because current voice tools are frustrating to use and unreliable in real life. work in damm demos , break when people behave normally. people interrupt , change their mind mid sentences , they talk over the app  , pause , hesitate and fuckin restart
many of them are not handle this behavior 

The real problem :
problem is not speech recognition or text-to-speech quality. it's damm control , who is allowed to talk right now? , who must stop? what happens when both start at the same time? what happens when the user interrupts?
what happens when things happen too fast? existing tools leave this to the developer. every developer rewrites the same fragile logic. it breaks easily. what keeps happening today specially with me 

when adding voice to an app: audio overlaps , the app doesn’t stop talking , listening doesn’t restart cleanly , things hang or feel delayed , the system gets into a “confused” state , this makes voice features feel stupid and annoying.

I am fuckin tired of this shit.

this project is trying to fix : project exists to make voice interaction behave normally , means:

the app listens when the user speaks

the app stops speaking when the user interrupts

only one thing happens at a time

everything can be stopped instantly

the system never gets confused about what it’s doing

this project is about rules and control, not better voices
his project is NOT

This project is not:

a voice assistant

a chatbot

a speech model

a demo app

It is infrastructure that other voice features run on.

Success criteria (for me) :  will consider this project successful if: personally want to use it instead of existing voice tools ,  stop thinking about audio threads and edge cases

interrupting feels instant and natural nothing feels fragile ,  trust it enough to build other things on top of it , if i still feel the need to work around it, it has failed. i fuckin failed.

Guiding rule : 

if something feels annoying while using it,
that annoyance is the next thing to fix.

if it cannot be fixed cleanly,
the design is wrong.
