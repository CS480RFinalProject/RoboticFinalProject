import cv2
import numpy as np


class Gesture:

    def __init__(self, point):
        self.points = point

        self.finger1 = [2, 3, 4]
        self.finger2 = [6, 7, 8]
        self.finger3 = [10, 11, 12]
        self.finger4 = [14, 15, 16]
        self.finger5 = [18, 19, 20]
        self.joints = [2, 5, 9, 13, 17]

        self.fetch = ["finger1"]
        self.go = ["joins"]
        self.left = ["finger2", "finger3"]
        self.go_back = ["finger1", "finger2"]
        self.right = ["finger1", "finger2", "finger3"]
        self.spin = ["finger1", "finger2", "finger3", "finger4", "finger5"]
        # self.stop = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # -2,3 + 9,13

    def detect(self):
        s = "none"
        finger = []
        joint = False

        if len(set(self.finger1) & set(self.points)) > 0:
            finger.append("finger1")

        if len(set(self.finger2) & set(self.points)) > 0:
            finger.append("finger2")

        if len(set(self.finger3) & set(self.points)) > 0:
            finger.append("finger3")

        if len(set(self.finger4) & set(self.points)) > 0:
            finger.append("finger4")

        if len(set(self.finger5) & set(self.points)) > 0:
            finger.append("finger5")

        if len(set(self.joints) & set(self.points)) > 0:
            joint = True

        if joint:
            s = "go"
        if self.fetch == finger:
            s = "fetch"
        if self.spin == finger:
            s = "spin"
        if self.left == finger:
            s = "left"
        if self.go_back == finger:
            s = "go_back"
        if self.right == finger:
            s = "right"
        return s
