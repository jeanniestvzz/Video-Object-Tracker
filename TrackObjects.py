import cv2

print("")
print("MANUALLY DETECT AND TRACK OBJECTS THROUGH VIDEO")
print("")

# RUN WEBCAM AND CAPTURE FRAMES 
cap = cv2.VideoCapture(0)

print("")
print("Select a tracker from the options below: ")
print("")
print("1. MOSSE")
print("2. CSRT")
print("3. BOOSTING")
print("4. MIL")
print("5. KCF")
print("6. TLD")
print("7. MEDIANFLOW")
print("")

t = input()
t = int(t)

# TRACKER
if t == 1:
    tracker = cv2.legacy_TrackerMOSSE.create()
elif t == 2:
    tracker = cv2.legacy_TrackerCSRT.create()
elif t == 3:
    tracker = cv2.legacy_TrackerBoosting.create()
elif t == 4:
    tracker = cv2.legacy_TrackerMIL.create()
elif t == 5:
    tracker = cv2.legacy_TrackerKCF.create()
elif t == 6:
    tracker = cv2.legacy_TrackerTLD.create()
elif t == 7:
    tracker = cv2.legacy_TrackerMedianFlow.create()
else:
    print("Not an option. Bye!")
    exit()

success, vid = cap.read()

# INITIALIZE BOUNDING BOX
bounding_box = cv2.selectROI("Tracking", vid, False)

# INITIALIZE TRACKER
tracker.init(vid, bounding_box)

def drawBox(vid, bounding_box):
    # COORDINATES
    w = int(bounding_box[0])
    x = int(bounding_box[1])
    y =  int(bounding_box[2])
    z = int(bounding_box[3])

    # CREATE BOX
    box_color = (255,0,255)
    top_left = (w, x)
    bottom_right = ((w + y), (x + z))
    thickness = 3
    line_type = 1
    cv2.rectangle(vid, top_left, bottom_right, box_color, thickness, line_type)

    # DISPLAY TEXT
    text_location = (75,100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    text_color = (0,255,0)
    cv2.putText(vid, "Tracking", text_location, font, scale, text_color, 2)

while True:
    success, vid = cap.read()

    # TIMER
    timer = cv2.getTickCount()

    # CONTINUE TRACKING -> UPDATE TRACKER
    success, bounding_box = tracker.update(vid)

    # TEXT LOCATION
    fps_text_location = (75,50)
    lost_text_location = (75,100)
    # FONT
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    text_color = (0,0,255)
    thickness = 2

    # IF IMAGE STILL APPEARS IN CAMERA, DRAW BOX ON IT
    if success:
        drawBox(vid, bounding_box)
    # IF IMAGE IS NOT IN CAMERA, SAY IT IS LOST
    else:
        cv2.putText(vid, "Lost", lost_text_location, font, scale, text_color, thickness)

    # GET FRAMES PER SECOND
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    fps = int(fps)    

    # ADD TEXT TO DISPLAY FRAMES PER SECOND
    cv2.putText(vid, str(fps), fps_text_location, font, scale, text_color, thickness)
    img = cv2.resize(vid, (0,0), fx = 0.75, fy = 0.75)
    cv2.imshow("Frame", vid)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()