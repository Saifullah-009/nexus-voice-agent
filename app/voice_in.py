import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import os
import tempfile
import time

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
SILENCE_THRESHOLD = 300
SILENCE_DURATION = 0.35        # Fast silence cutoff

def listen_to_user():
    audio_frames = []
    has_spoken = False
    silence_start = None
    start_time = time.time()
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
        while True:
            data, _ = stream.read(CHUNK_SIZE)
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = np.abs(audio_data).mean()
            audio_frames.append(audio_data)

            if energy > SILENCE_THRESHOLD:
                has_spoken = True
                silence_start = None
            elif has_spoken:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION:
                    break
            
            if not has_spoken and (time.time() - start_time > 4.0):
                return "", 0.0
            
            if time.time() - start_time > 8.0:
                break

    if not has_spoken or len(audio_frames) == 0:
        return "", 0.0

    temp_wav = os.path.join(tempfile.gettempdir(), "nexus_input.wav")
    complete_audio = np.concatenate(audio_frames, axis=0)
    wav.write(temp_wav, SAMPLE_RATE, complete_audio)

    # Measure exact network transcription time
    stt_start = time.time()
    recognizer = sr.Recognizer()
    text = ""
    try:
        with sr.AudioFile(temp_wav) as source:
            recorded_audio = recognizer.record(source)
            text = recognizer.recognize_google(recorded_audio)
    except Exception:
        text = ""
    finally:
        stt_elapsed = time.time() - stt_start
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception:
                pass

    return text, stt_elapsed