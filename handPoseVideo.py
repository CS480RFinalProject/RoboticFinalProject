import cv2
import time
import numpy as np
from handPoseImage import ReadImage
from defectDetect import Defect


class Video:
    def __init__(self):
        self.cap = cv2.VideoCapture(-1)
        self.hand = 6
        self.t0 = 0
        self.type = None

    def getType(self):
        while self.type is None:
            self.type = raw_input("For laps enter l, for command enter c: ")
        result = self.capture()
        return result

    def capture(self):
        self.t0 = time.time()
        result = None
        rArray = []
        while self.hand > 0:
            hasFrame, frame = self.cap.read()
            if not hasFrame:
                cv2.waitKey()
                break
            cv2.rectangle(frame, (300, 300), (100, 100), (0, 255, 0), 0)
            crop_img = frame[100:300, 100:300]
            t = time.time() - self.t0
            if t > 10:
                if self.type == 'l':
                    obj = Defect(crop_img)
                    result = obj.detect()
                else:
                    obj = ReadImage(crop_img)
                    result = obj.imgRead()
                self.hand -= 1
                self.t0 = time.time()
                rArray.append(result)
            else:
                # show the gesture
                s = "show the gesture: % d" % (10 - t)
                cv2.putText(frame, s, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
        print("x")
        return rArray


def main():
    obj = Video()  # runs the actual algorithm
    rArray = obj.getType()
    with open('file.txt', 'w') as f:
        for result in rArray:
            f.write("%s\n" % result)
    print(result)
    print("XX")


if __name__ == '__main__':
    main()
