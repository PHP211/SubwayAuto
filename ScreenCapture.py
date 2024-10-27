import cv2
import numpy as np
import mss
import time
from collections import deque
import keyboard  # Thư viện cho phép bắt sự kiện bàn phím
import os  # Thư viện để làm việc với thư mục

# Thiết lập số khung hình và kích thước bộ đệm
FRAME_RATE = 20.0
BUFFER_SIZE = 8  # Số lượng khung hình cần lưu

# Thư mục gốc để lưu các video
BASE_DIRECTORY = "PROJECT2/data"

# Tự động lấy độ phân giải màn hình từ mss
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Thường màn hình chính là monitors[1]
    SCREEN_WIDTH = monitor["width"]
    SCREEN_HEIGHT = monitor["height"]
    screen_dimensions = {
        "top": monitor["top"],
        "left": monitor["left"],
        "width": SCREEN_WIDTH,
        "height": SCREEN_HEIGHT
    }

# Sử dụng deque để lưu các khung hình gần nhất
frame_buffer = deque(maxlen=BUFFER_SIZE)

# Tạo các thư mục con trong thư mục gốc nếu chưa tồn tại
os.makedirs(os.path.join(BASE_DIRECTORY, "up"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIRECTORY, "down"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIRECTORY, "left"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIRECTORY, "right"), exist_ok=True)

# Bắt đầu quá trình quay màn hình
with mss.mss() as sct:
    while True:
        # Chụp ảnh màn hình và chuyển đổi thành array NumPy
        img = np.array(sct.grab(screen_dimensions))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Thêm khung hình vào bộ đệm
        frame_buffer.append(frame)

        # Hiển thị khung hình để theo dõi
        cv2.imshow("Screen Recorder", frame)
        
        # Kiểm tra các phím mũi tên
        if keyboard.is_pressed("up"):
            folder = "up"
        elif keyboard.is_pressed("down"):
            folder = "down"
        elif keyboard.is_pressed("left"):
            folder = "left"
        elif keyboard.is_pressed("right"):
            folder = "right"
        else:
            folder = None
        
        # Nếu một trong các phím mũi tên được nhấn, lưu video vào thư mục tương ứng
        if folder:
            # Tạo đối tượng VideoWriter để lưu file video
            timestamp = int(time.time())
            output_filename = os.path.join(BASE_DIRECTORY, folder, f"recording_{timestamp}.avi")
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(output_filename, fourcc, FRAME_RATE, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Ghi tất cả khung hình trong bộ đệm vào file video
            for buffered_frame in frame_buffer:
                out.write(buffered_frame)
            
            # Giải phóng đối tượng ghi video sau khi ghi xong
            out.release()
            print(f"Lưu video vào thư mục {folder} trong {BASE_DIRECTORY}: {output_filename}")
            
        # Thoát nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Đóng cửa sổ hiển thị
cv2.destroyAllWindows()
