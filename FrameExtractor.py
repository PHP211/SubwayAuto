import cv2
import os

def FrameExtraction(videoPath, outputDir, numberOfFrames, imageSize=(224, 224)):
    # Create output directory if it doesn't exist
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
        # normalizedFrame = resizedFrame / 255.0
        framesList.append(frame)

        # Save the frame as an image in the output directory
        frameFilename = os.path.join(outputDir, f"frame_{frameCounter}.jpg")
        cv2.imwrite(frameFilename, frame)

    videoReader.release()
    return framesList

frames = FrameExtraction("recording_1730027190.avi", "output_frames", numberOfFrames=8, imageSize=(224, 224))
print(len(frames))