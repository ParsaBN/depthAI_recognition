import cv2
import numpy as np

# import rospy
# import std_msgs as msg

# def talker(box):
#     pub = rospy.Publisher('bbox', msg.Int32MultiArray, queue_size = 20)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(20)
#     while not rospy.is_shutdown():
#         bbox_arr = box
#         rospy.loginfor(bbox_arr)
#         pub.publish(bbox_arr)
#         rate.sleep()

cap = cv2.VideoCapture(0)
whT = 320
confThreshold = 0.4
nmsThreshold = 0.3 # the lower the more aggressive and the less no. of boxes

classeNames = ['person']

# classesFile = 'class.names'
# classNames = []
# with open(classesFile, 'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')


modelConfiguration = 'detection_models/yolov3-tiny.cfg'
modelWeights = 'detection_models/yolov3-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObject(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2]*wT), int(det[3]*hT)
                x, y = int((det[0]*wT) - (w/2)), int((det[1]*hT) - (h/2))
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        # print(box)
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
        cv2.putText(img, f'PERSON {int(confs[i]*100)}%', 
            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        # {classNames[classIds[i]].upper()} if more classes instead of PERSON
        # if __name__ == '__main__':
        #     try:
        #         talker(box)
        #     except rospy.ROSInterruptException:
        #         pass
    # print("...........")


while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(outputNames)

    findObject(outputs, img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    