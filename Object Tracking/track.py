# importing necessary packages
import numpy as np
import argparse
import cv2 

# intialize the current frame of the video along with the list
#ROI points along with whether or not this is input mode

frame = None              #The current frame of the video
roiPts = []               #list of points corresponding the (ROI) of the video
inputMode = False         #indicates whether or not we are currently selecting an object

# selecting ROI (selectROI WILL BE USED TO SELECT ROI TRACKING)
def selectROI(event, x, y, flags, param):  #Grabs reffrence to the current frame
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4: #if we are in ROI selection mode the mouse was clicked and we do not already have 4 pointsthen apdate the list of ROI points with the (x,y ) location of the click and drow the circle
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)


def main():
    # construct the argument parse and parse the arguments
   ap = argparse.ArgumentParser()
   ap.add_argument("-v", "--video", 
                   help= "path to the (optional) video file")
args = vars(ap.parse_args())
    # grab the reffrence of the current frame , list of ROI (Region Of Intrest) points and whether or not it is ROI selection mode global frame, roipts, inputMode
    #if the video path was not supplied, grab the reffrence to the camera

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    #otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

# setup the mouse callback
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", selectROI)

#intialize the terminal criteria for cam shift,indicating a maximum of ten iteration or movemeent by a least on pxiel along with the bounding box of the ROI

terminal = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
roiBox = None

#keep looping over the framees

while True:
    (grabbed, frame) = camera.read()   #grab the current frame

    if not grabbed:    #check to see if we have reached the end of the video
        break

    #if the see in the ROI  has been camputed
    if roiBox is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGR)   #convert the current frame to the HSV color space and perform mean shift
        backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
        (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)  #apply Cam Shift to the back projection, convert the points to a bounding box, and then drow theem 
        pts = np.int0(cv2.cv.BoxPoints(r))
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2) 

        #show the frame and record if the user presses a key
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF

        #Handle if the 'i' key is pressed, then go into ROI selected mode
    if key == ord("i") and len(roiPts) < 4:
        inputMode = True     #indicate that we are in input mode and clone the frame
        orig = frame.copy()

        #keep looping untill 4 reference ROI points have been selected; press any key to exict ROI selection mode once 4 points have been selected
    while len(roiPts) <4:
        cv2.imshow("frame", frame)
        cv2.waitKey(0)

        #determine the top-leeft and bottom-right points
    roiPts = np.array(roiPts)
    s = roiPts.sum(axis = 1)
    tl = roiPts[np.argmin(5)]
    br = roiPts[np.argmax(5)]

         # grab the ROI for the bounding box and convert it to the HSV color space
    roi = orig[tl[1]:br[1], tl[0]:br[0]] 
    roi = cv2.cvtColor(roi, cv2.COLOR_BAYER_BG2RGB)

        #Compute a HSV histogram for the ROI and store the bounding box
    roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
    roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
    roiBox = (tl[0], tl[1], br[0], br[1])

       # IF  the 'q' key is pressed, stop the loop
       elif key == ord("q"):
   break

    # cleanup the camera and clouse any open windows
camera.release()
cv2.destroyAllWindows()

if__name__ =="__main__":
  main()
