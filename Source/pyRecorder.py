import pygame
import os
from datetime import datetime

class Recorder():
    def __init__(self):
        #create the recording folder
        baseFolder = "recording"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.saveFolder = baseFolder + "_" + str(timestamp)
        os.makedirs(self.saveFolder, exist_ok=True)

    def takeShot(self, surface, shotIndex):
        #frame format example: frame_00320.png
        framename = "frame_" + "0"*(5-len(str(shotIndex))) + str(shotIndex) + ".png"
        fullpath = os.path.join(self.saveFolder, framename)
        pygame.image.save(surface, fullpath)

    def compileToVideo(self, framerate_):
        import cv2

        output = self.saveFolder + ".avi"

        frames = sorted([f for f in os.listdir(self.saveFolder) if f.endswith(".png")])
        first_frame = cv2.imread(os.path.join(self.saveFolder, frames[0]))
        height, width, _ = first_frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Lossless-ish, widely supported
        out = cv2.VideoWriter(output, fourcc, 60, (width, height))

        for f in frames:
            img_path = os.path.join(self.saveFolder, f)
            img = cv2.imread(img_path)
            out.write(img)

        out.release()