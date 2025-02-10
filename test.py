import asyncio
import websockets
import wave

async def stream_audio():
    uri = "ws://localhost:8004"  # Adjust if your server is on another machine.
    async with websockets.connect(uri) as websocket:
        # Open the WAV file and read its audio frames
        with wave.open("/home/torrobot/robotcontrol-pi5/uploads/recorded_audio.wav", "rb") as wf:
            # Optional: Verify that file parameters match your server's configuration.
            channels = wf.getnchannels()
            rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            print(f"File parameters: Channels={channels}, Rate={rate}, Sample Width={sample_width}")

            chunk_size = 1024
            data = wf.readframes(chunk_size)
            while data:
                await websocket.send(data)
                # Sleep for the duration of the chunk to simulate real-time streaming.
                await asyncio.sleep(chunk_size / rate)
                data = wf.readframes(chunk_size)

asyncio.run(stream_audio())
