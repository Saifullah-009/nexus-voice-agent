import os
import edge_tts
from playsound3 import playsound

VOICE = "en-US-ChristopherNeural"
OUTPUT_FILE = os.path.abspath("nexus_speech.mp3")

async def speak_text_direct(text: str) -> float:
    """Generates audio and forces direct hardware speaker output."""
    communicate = edge_tts.Communicate(text, VOICE, rate="+20%")
    await communicate.save(OUTPUT_FILE)
    
    # Play directly to hardware audio device
    playsound(OUTPUT_FILE)
    
    return 1.0