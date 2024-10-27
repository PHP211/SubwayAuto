import cv2
import os

def FrameExtraction(videoPath, outputDir, numberOfFrames, imageSize=(224, 224)):
    # Tạo thư mục đích nếu chưa tồn tại
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        
    framesList = []
    videoReader = cv2.VideoCapture(videoPath)
    framesCount = int(videoReader.get(cv2.CAP_PROP_FRAME_COUNT))
    skipFrame = max(int(framesCount / numberOfFrames), 1)

    for frameCounter in range(numberOfFrames):
        videoReader.set(cv2.CAP_PROP_POS_FRAMES, frameCounter * skipFrame)

        success, frame = videoReader.read()

        if not success:
            break

        # Resize and normalize the frame
        # resizedFrame = cv2.resize(frame, imageSize)
        framesList.append(frame)

        # Lưu khung hình dưới dạng ảnh trong thư mục đích
        frameFilename = os.path.join(outputDir, f"frame_{frameCounter}.jpg")
        cv2.imwrite(frameFilename, frame)

    videoReader.release()
    return framesList

def ProcessAllVideosInFolder(inputFolder, outputFolder, numberOfFrames=8, imageSize=(224, 224)):
    # Duyệt qua tất cả các file trong thư mục nguồn
    for root, _, files in os.walk(inputFolder):
        for file in files:
            # Chỉ xử lý các file có phần mở rộng là .avi (hoặc .mp4 nếu cần)
            if file.endswith(".avi"):
                videoPath = os.path.join(root, file)

                # Tạo đường dẫn thư mục đích tương tự trong outputFolder
                relativePath = os.path.relpath(root, inputFolder)
                outputDir = os.path.join(outputFolder, relativePath, os.path.splitext(file)[0])

                # Trích xuất khung hình và lưu vào thư mục đích
                print(f"Processing video: {videoPath}")
                FrameExtraction(videoPath, outputDir, numberOfFrames, imageSize)

# Thư mục chứa các video gốc
inputFolder = "PROJECT2/data/up"
# Thư mục đích để lưu khung hình
outputFolder = "extracted_frames"

# Thực hiện trích xuất khung hình từ tất cả các video trong inputFolder
ProcessAllVideosInFolder(inputFolder, outputFolder, numberOfFrames=8, imageSize=(224, 224))
