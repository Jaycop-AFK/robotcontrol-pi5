# import cv2
# import asyncio
# import websockets
# from threading import Thread

# latest_frame = None

# async def send_video(websocket):
#     global latest_frame
#     while True:
#         if latest_frame is not None:
#             await websocket.send(latest_frame)
#         await asyncio.sleep(0.03) 

# def capture_frames():
#     global latest_frame
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Failed to capture video frame.")
#                 break
#             _, jpeg = cv2.imencode('.jpg', frame)
#             latest_frame = jpeg.tobytes()
#     finally:
#         cap.release()

# def start_video_capture():
#     video_thread = Thread(target=capture_frames)
#     video_thread.daemon = True
#     video_thread.start()

# async def main():
#     start_video_capture()
#     async with websockets.serve(send_video, "0.0.0.0", 8001):
#         print("Video WebSocket server started on ws://0.0.0.0:8001")
#         await asyncio.Future() 

# if __name__ == "__main__":
#     asyncio.run(main())


import cv2
import asyncio
import websockets
from threading import Thread

latest_frame = None

async def send_video(websocket):
    global latest_frame
    while True:
        if latest_frame is not None:
            await websocket.send(latest_frame)
        await asyncio.sleep(0.03)  # Maintain ~33 FPS for responsiveness

def capture_frames():
    global latest_frame
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video frame.")
                break
            # Resize frame to 144p
            resized_frame = cv2.resize(frame, (256, 144))
            _, jpeg = cv2.imencode('.jpg', resized_frame)
            latest_frame = jpeg.tobytes()
    finally:
        cap.release()

def start_video_capture():
    video_thread = Thread(target=capture_frames)
    video_thread.daemon = True
    video_thread.start()

async def main():
    start_video_capture()
    async with websockets.serve(send_video, "0.0.0.0", 8001):
        print("Video WebSocket server started on ws://0.0.0.0:8001")
        await asyncio.Future()  # Keep the server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())
