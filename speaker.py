# import asyncio
# import websockets
# import pyaudio
# import numpy as np
# from scipy.signal import butter, lfilter

# # Audio configuration constants
# AUDIO_FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 4096
# VOLUME_MULTIPLIER = 1.3  # เพิ่มตัวคูณเสียงเพื่อให้เสียงดังขึ้น

# def butter_bandpass(lowcut, highcut, fs, order=5):
#     """สร้าง coefficients สำหรับ band-pass filter ด้วย Butterworth filter"""
#     nyq = 0.5 * fs
#     low = lowcut / nyq
#     high = highcut / nyq
#     b, a = butter(order, [low, high], btype='band')
#     return b, a

# def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
#     """ประยุกต์ใช้ band-pass filter กับข้อมูลเสียง"""
#     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#     y = lfilter(b, a, data)
#     return y

# def create_audio_stream():
#     """Initialize and return a PyAudio stream for audio playback."""
#     audio = pyaudio.PyAudio()
#     stream = audio.open(
#         format=AUDIO_FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         output=True
#     )
#     return audio, stream

# async def handle_audio_stream(websocket):
#     """Handle incoming audio data from the WebSocket and play it back."""
#     audio, stream = create_audio_stream()
#     try:
#         print("Client connected.")
#         async for message in websocket:
#             print(f"Received message length: {len(message)} bytes")  # Log ความยาวข้อมูล

#             try:
#                 # แปลงข้อมูลที่ได้รับเป็น numpy array
#                 audio_data = np.frombuffer(message, dtype=np.int16)
#                 print(f"Audio data preview: {audio_data[:10]}")  

                
#                 filtered_audio_data = apply_bandpass_filter(audio_data, 300, 3400, RATE, order=6)

                
#                 amplified_audio_data = np.clip(filtered_audio_data * VOLUME_MULTIPLIER, -32768, 32767).astype(np.int16)
                
#                 stream.write(amplified_audio_data.tobytes())
#             except Exception as e:
#                 print(f"Error processing audio data: {e}")

#     except websockets.ConnectionClosed:
#         print("WebSocket connection closed.")
#     finally:
#         stream.stop_stream()
#         stream.close()
#         audio.terminate()
#         print("Audio stream closed.")

# async def start_server():
#     """Start the WebSocket server for audio streaming."""
#     server = await websockets.serve(handle_audio_stream, "0.0.0.0", 8004)
#     print("WebSocket server running on ws://0.0.0.0:8004")
#     await server.wait_closed()

# if __name__ == "__main__":
#     asyncio.run(start_server())


from fastapi import FastAPI, Request
import uvicorn
import pyaudio
import numpy as np
from scipy.signal import butter, lfilter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือระบุ origin ที่อนุญาต เช่น ["http://10.10.15.44"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# กำหนดค่าคอนฟิกของเสียง
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
VOLUME_MULTIPLIER = 1.3  # เพิ่มตัวคูณเสียง

def butter_bandpass(lowcut, highcut, fs, order=5):
    """สร้าง coefficients สำหรับ band-pass filter ด้วย Butterworth filter"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """ประยุกต์ใช้ band-pass filter กับข้อมูลเสียง"""
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# สร้าง PyAudio stream สำหรับการเล่นเสียง (เปิดใช้งานเพียงครั้งเดียว)
audio = pyaudio.PyAudio()
stream = audio.open(
    format=AUDIO_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True
)

@app.post("/audio")
async def receive_audio(request: Request):
    """รับข้อมูลเสียงผ่าน HTTP POST และเล่นออกเสียง"""
    data = await request.body()  # รับข้อมูล binary ทั้งหมดใน body
    print(f"Received {len(data)} bytes of audio data")
    try:
        # แปลงข้อมูลที่รับมาเป็น numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        print("Audio data preview:", audio_data[:10])
        
        # กรองเสียงด้วย bandpass filter
        filtered_audio_data = apply_bandpass_filter(audio_data, 300, 3400, RATE, order=6)
        
        # ขยายเสียง (amplify) โดยคูณและจำกัดค่าผ่าน np.clip
        amplified_audio_data = np.clip(filtered_audio_data * VOLUME_MULTIPLIER, -32768, 32767).astype(np.int16)
        
        # เล่นเสียงออกทาง output device
        stream.write(amplified_audio_data.tobytes())
        return {"status": "ok"}
    except Exception as e:
        print("Error processing audio data:", e)
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
