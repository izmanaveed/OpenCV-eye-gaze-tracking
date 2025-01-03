import cv2 as cv
import numpy as np
#import time
import cv_proj2_func as m

COUNTER = 0
TOTAL_BLINKS = 0
CLOSED_EYES_FRAME = 3
cameraID = 0
videoPath = "Video/abc.mp4"
# variables for frame rate.
FRAME_COUNTER = 0
#START_TIME = time.time()
#FPS = 0
POSITION=" "

# creating camera object
camera = cv.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
f = camera.get(cv.CAP_PROP_FPS)
width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)
print(width, height, f)
fileName = videoPath.split('/')[1]
name = fileName.split('.')[0]
print(name)

while True:
    FRAME_COUNTER += 1
    # getting frame from camera
    ret, frame = camera.read()
    if ret == False:
        break

    # converting frame into Gry image.
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = grayFrame.shape
    circleCenter = (int(width/2), 50)
    # calling the face detector funciton
    image, face = m.faceDetector(frame, grayFrame)
    if face is not None:

        # calling landmarks detector funciton.
        image, PointList = m.faceLandmarkDetector(frame, grayFrame, face, False)
        # print(PointList)

        #cv.putText(frame, f'FPS: {round(FPS,1)}',(460, 20), m.fonts, 0.7, m.YELLOW, 2)
        RightEyePoint = PointList[36:42]
        LeftEyePoint = PointList[42:48]
        leftRatio, topMid, bottomMid = m.blinkDetector(LeftEyePoint)
        rightRatio, rTop, rBottom = m.blinkDetector(RightEyePoint)
       # cv.circle(image, topMid, 2, m.YELLOW, -1)
       # cv.circle(image, bottomMid, 2, m.YELLOW, -1)

        blinkRatio = (leftRatio + rightRatio)/2
        cv.circle(image, circleCenter, (int(blinkRatio*4.3)), m.CHOCOLATE, -1)
        cv.circle(image, circleCenter, (int(blinkRatio*3.2)), m.CYAN, 2)
        cv.circle(image, circleCenter, (int(blinkRatio*2)), m.GREEN, 3)

        if blinkRatio > 4:
            COUNTER += 1
            cv.line(image, (25, 50), (110, 50), m.WHITE, 30)
            cv.putText(image, f'Blink', (35, 55), m.fonts, 0.8, m.PURPLE, 2)
            print("blink")
        else:
            if COUNTER > CLOSED_EYES_FRAME:
                TOTAL_BLINKS += 1
                COUNTER = 0
        cv.putText(image, f'Total Blinks: {TOTAL_BLINKS}', (230, 17), m.fonts, 0.5, m.ORANGE, 2)

        # for p in LeftEyePoint:
        #     cv.circle(image, p, 3, m.MAGENTA, 1)
        mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
        #maskleft, leftPos, leftColor = m.EyeTracking(
        #    frame, grayFrame, LeftEyePoint)

        # draw background as line where we put text.
        cv.line(image, (30, 90), (100, 90), color[0], 30)  

        # writing text on above line
        cv.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)
        POSITION=pos

        # showing the frame on the screen
        cv.imshow('Frame', image)
    else:
        cv.imshow('Frame', frame)

    # Recoder.write(frame)
    # calculating the seconds
    #SECONDS = time.time() - START_TIME
    # calculating the frame rate
    #FPS = FRAME_COUNTER/SECONDS
    # print(FPS)

    print(POSITION)
    key = cv.waitKey(1)

    # if q is pressed on keyboard: quit
    if key == ord('q'):
        break
# closing the camera
camera.release()

# closing  all the windows
cv.destroyAllWindows()
