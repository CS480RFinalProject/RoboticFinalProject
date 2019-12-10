from __future__ import division
import cv2
import time
import numpy as np
from gestureDetection import Gesture

# call dot detector and return the conclusion
class ReadImage:

    def __init__(self, orgFrame):
        self.protoFile = "hand/pose_deploy.prototxt"
        self.weightsFile = "hand/pose_iter_102000.caffemodel"
        self.nPoints = 22
        self.frame = orgFrame

    def imgRead(self):

        net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsFile)
        frameCopy = np.copy(self.frame)
        frameWidth = self.frame.shape[1]
        frameHeight = self.frame.shape[0]
        aspect_ratio = frameWidth/frameHeight

        threshold = 0.25

        t = time.time()
        # input image dimensions for the network
        inHeight = 368
        inWidth = int(((aspect_ratio*inHeight)*8)//8)
        inpBlob = cv2.dnn.blobFromImage(self.frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

        net.setInput(inpBlob)

        output = net.forward()
        print("time taken by network : {:.3f}".format(time.time() - t))

        # Empty list to store the detected keypoints
        points = []

        for i in range(self.nPoints):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]
            probMap = cv2.resize(probMap, (frameWidth, frameHeight))

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            if prob > threshold :
                cv2.circle(frameCopy, (int(point[0]), int(point[1])), 1, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frameCopy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, lineType=cv2.LINE_AA)

                # Add the point to the list if the probability is greater than the threshold
                # Will be used when gesture is tried to be classified
                points.append(i)
            else :
                points.append(None)


        cv2.imshow('Output-Keypoints', frameCopy)
        cv2.imshow('Output-Skeleton', self.frame)

        print("Total time taken : {:.3f}".format(time.time() - t))

        with open('file.txt', 'w') as f:
            for item in point:
                f.write("%s\n" % item)
        cv2.waitKey(5)
        obj = Gesture(points)
        result = obj.detect()
	print(result)
        return result


def main():
    img = cv2.imread('p/9.png')
    obj = ReadImage(img) # runs the actual algorithm
    result = obj.imgRead()
    print(result)
    #cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
