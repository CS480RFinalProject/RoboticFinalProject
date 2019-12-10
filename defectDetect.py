import cv2
import time
import numpy as np
import imutils
import math


class Defect:
    def __init__(self, orgFrame):
        self.min_YCrCb = np.array([0, 133, 77], np.uint8)
        self.max_YCrCb = np.array([235, 173, 127], np.uint8)
        self.frame = orgFrame
        self.detect()

    def detect(self):

        imageYCrCb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YCR_CB)
        skinMask = cv2.inRange(imageYCrCb, self.min_YCrCb, self.max_YCrCb)
        grey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #cv2.imshow('Thresholded', thresh1)
        contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        max_area = -1
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_area = area
                ci = i
        cnt = contours[ci]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(self.frame.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(self.frame, far, 1, [0, 0, 255], -1)
            # dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(self.frame, start, end, [0, 255, 0], 2)
        if count_defects == 1:
            print(2)
            return 2
        elif count_defects == 2:
            print(3)
            return 3
        elif count_defects == 3:
            print(4)
            return 4
        elif count_defects == 4:
            print(5)
            return 5
        else:
            a=0
        cv2.imshow('Gesture', self.frame)
        cv2.waitKey(0)

