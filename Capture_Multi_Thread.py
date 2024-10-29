from pynput import keyboard
import os
from datetime import datetime
import time 
from threading import Thread
import cv2
import mss
import numpy as np
from collections import deque



# Tạo các thư mục nếu chưa tồn tại
os.makedirs("data/up", exist_ok=True)
os.makedirs("data/right", exist_ok=True)
os.makedirs("data/left", exist_ok=True)
os.makedirs("data/down", exist_ok=True)
os.makedirs("data/auto", exist_ok=True)

# Giới hạn kích thước của frames để lưu tối đa 10 khung hình gần nhất
MAX_SIZE = 10
BACK_FRAME = 5
frames = deque(maxlen=MAX_SIZE)



def createNewSetFolder(state):
    timestamp_folder = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_dir = f"data/{state}/{timestamp_folder}"
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def save_images(frames, save_dir):
    for i, frame in enumerate(frames):
        frame_filename = os.path.join(save_dir, f"{i + 1}.jpg")
        cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    print(f"Tất cả ảnh đã được lưu vào {save_dir}")

def auto_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True :
            # Capture the screen
            screenshot = sct.grab(monitor)
            frame_resized = cv2.cvtColor( cv2.resize( np.array(screenshot), (0, 0), fx=0.3, fy=0.3) , cv2.COLOR_BGRA2GRAY)
            frames.append(frame_resized)
            

def capture_with_state(state):
    buffer = list(frames)[-5:]
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        for _ in range(5):
            screenshot = sct.grab(monitor)
            frame_resized = cv2.cvtColor( cv2.resize( np.array(screenshot), (0, 0), fx=0.3, fy=0.3) , cv2.COLOR_BGRA2GRAY)
            buffer.append(frame_resized)
        
        save_dir = createNewSetFolder(state)
        save_thread = Thread(target=save_images, args=(list(buffer), save_dir))
        save_thread.start()
        save_thread.join()
    

# Hàm xử lý khi một phím được nhấn
def on_press(key):
    try:
        # Nếu phím mũi tên lên được nhấn, chụp màn hình và lưu vào thư mục up
        if key == keyboard.Key.up:
            Thread(target=capture_with_state, args=["up"]).start()

        # Nếu phím mũi tên phải được nhấn, chụp màn hình và lưu vào thư mc right
        elif key == keyboard.Key.right:
            Thread(target=capture_with_state, args=["right"]).start()

        # Nếu phím mũi tên xuống được nhấn, chụp màn hình và lưu vào thư mục down
        elif key == keyboard.Key.down:
            Thread(target=capture_with_state, args=["down"]).start()
            
            
        elif key == keyboard.Key.left:
            Thread(target=capture_with_state , args=["left"]).start()

    except AttributeError:
        pass

def start_recording():
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("Recording stopped.")

capture_thread = Thread(target=auto_screenshot)
capture_thread.start()

start_recording()