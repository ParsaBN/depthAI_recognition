# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascades", type=str, default="cascades",
	help="path to input directory containing haar cascades")
args = vars(ap.parse_args())

# initialize a dictionary that maps the name of the haar cascades to
# their filenames
detectorPaths = {
	"face": "haarcascade_frontalface_default.xml",
    "fullbody": "haarcascade_fullbody.xml"
}
# initialize a dictionary to store our haar cascade detectors
print("[INFO] loading haar cascades...")
detectors = {}
# loop over our detector paths
for (name, path) in detectorPaths.items():
	# load the haar cascade from disk and store it in the detectors
	# dictionary
	path = os.path.sep.join([args["cascades"], path])
	detectors[name] = cv2.CascadeClassifier(path)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    # grab the frame from the video stream, resize it, and convert it
    # to grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # perform face detection using the appropriate haar cascade
    faceRects = detectors["face"].detectMultiScale(
        gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # loop over the face bounding boxes
    for (fX, fY, fW, fH) in faceRects:
        # extract the face ROI
        faceROI = gray[fY:fY+ fH, fX:fX + fW]
        # draw the face bounding box on the frame
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH),
            (0, 255, 0), 2)

    # bodyRects = detectors["fullbody"].detectMultiScale(
    #     gray, scaleFactor=1.05, minNeighbors=4,
    #     minSize=(30, 10)
    # )
    # # loop over the body bounding boxes
    # for (bX, bY, bW, bH) in bodyRects:
    #     # extract the bodb ROI
    #     bodyROI = gray[bY:bY+ bH, bX:bX + bW]
    #     # draw the body bounding box on the frame
    #     cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
    #         (0, 255, 255), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()