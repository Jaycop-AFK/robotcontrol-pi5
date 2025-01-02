import asyncio
import websockets
import pyaudio
import numpy as np

# Audio configuration constants
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
VOLUME_MULTIPLIER = 1.5  # เพิ่มตัวคูณเสียงเพื่อให้เสียงดังขึ้น

def create_audio_stream():
    """Initialize and return a PyAudio stream for audio playback."""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True
    )
    return audio, stream

async def handle_audio_stream(websocket):
    """Handle incoming audio data from the WebSocket and play it back."""
    audio, stream = create_audio_stream()
    try:
        print("Client connected.")
        async for message in websocket:
            print(f"Received message length: {len(message)} bytes")  # Log message length

            # Convert message to numpy array
            try:
                audio_data = np.frombuffer(message, dtype=np.int16)
                print(f"Audio data preview: {audio_data[:10]}")  # Log preview of the data

                # เพิ่มระดับเสียงโดยการคูณด้วย VOLUME_MULTIPLIER
                amplified_audio_data = np.clip(audio_data * VOLUME_MULTIPLIER, -32768, 32767).astype(np.int16)
                
                stream.write(amplified_audio_data.tobytes())
            except Exception as e:
                print(f"Error processing audio data: {e}")

    except websockets.ConnectionClosed:
        print("WebSocket connection closed.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Audio stream closed.")

async def start_server():
    """Start the WebSocket server for audio streaming."""
    server = await websockets.serve(handle_audio_stream, "0.0.0.0", 8004)
    print("WebSocket server running on ws://10.10.16.65:8004")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
