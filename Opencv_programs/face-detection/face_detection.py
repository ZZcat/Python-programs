# Imports start
import time
from datetime import date
import getpass
#tandd = "Time :",time.strftime("%I:%M:%S"),"   Date:",(time.strftime("%d/%m/%Y")),"     ","User: ",getpass.getuser(), "\n"
x = 0
print "Loading numpy..."
import numpy as np
time.sleep(x)
print "Loaded numpy as np\n"
print "Loading open-cv..."
import cv2
time.sleep(x)
print "Loaded cv2\n"
print "Loading open-cv files..."
import cv2.cv as cv
time.sleep(x)
print "Loaded cv2.cv as cv\n"
print "Loading computer"
import sys
time.sleep(x)
print "Loaded sys\n"
print "Loading getopt"
import getopt
time.sleep(x)
print "loaded getopn\n"
print "Loaded all modules needed\n\n"
#  Imports ended
# Load files start
args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
args = dict(args)
print "Loading templates"
time.sleep(x)
cascade_fn = args.get('--cascade', "./haarcascade_frontalface_alt.xml")
nested_fn  = args.get('--nested-cascade', "./haarcascade_eye.xml")
cascade = cv2.CascadeClassifier(cascade_fn)
nested = cv2.CascadeClassifier(nested_fn)
print "Templates loaded\n\n"
# Load files ended
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
if __name__ == '__main__':
    try: video_src = video_src[0]
    except: video_src = 0
    cam = cv2.VideoCapture(0)
    while True:
        _, img = cam.read()    # Take each frame
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
         
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))

        

        if 0xFF & cv2.waitKey(5) == 27:
            print "Killing all windows"
            print "Shuting down"
            break
    cv2.destroyAllWindows()
#    with open("test.txt", "a") as myfile:
#       myfile.write("")
