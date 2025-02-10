import asyncio
import websockets
import pyaudio
import wave
import io

# Audio configuration constants
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096

def create_audio_input_stream():
    """Initialize and return a PyAudio stream for audio input."""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    return audio, stream

def encode_audio_to_wav(raw_audio):
    """Encode raw audio data to WAV format."""
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_writer:
        wav_writer.setnchannels(CHANNELS)
        wav_writer.setsampwidth(pyaudio.PyAudio().get_sample_size(AUDIO_FORMAT))
        wav_writer.setframerate(RATE)
        wav_writer.writeframes(raw_audio)
    return wav_buffer.getvalue()

async def send_audio(websocket):
    """Capture audio from the microphone and send it over WebSocket."""
    audio, stream = create_audio_input_stream()
    try:
        while True:
            raw_audio = stream.read(CHUNK, exception_on_overflow=False)
            wav_data = encode_audio_to_wav(raw_audio)
            await websocket.send(wav_data)
            await asyncio.sleep(0.01)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

async def start_server():
    """Start the WebSocket server for sending audio data."""
    server = await websockets.serve(send_audio, "0.0.0.0", 8002)
    print("Audio WebSocket server started on ws://0.0.0.0:8002")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())