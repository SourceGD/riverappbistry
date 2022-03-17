from imutils.video import FPS
import imutils
import cv2
import numpy as np

def stabilization(filepath,newName):
    vs = cv2.VideoCapture(filepath)
    ret, frame = vs.read()
    frame = imutils.resize(frame, width=920)
    (H, W) = frame.shape[:2]
    fps =  round(vs.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter('Video/'+newName,cv2.VideoWriter_fourcc(*'MP4V'), fps, (W,H)) 
    tracker1 = cv2.TrackerKCF_create()
    tracker2 = cv2.TrackerKCF_create()
    tracker3 = cv2.TrackerKCF_create()
    tracker4 = cv2.TrackerKCF_create()
    nTrack = 'kcf' 
    # initialize the bounding box coordinates of the object we are going
    # to track
    initBB = None
    fps = None
    centerInit = np.float32([[0,0],[0,0],[0,0],[0,0]])
    cnt = 1
    while(vs.isOpened()):
        
        if ret is True :
            # resize the frame (so we can process it faster) and grab the
            # frame dimensions
            frame = imutils.resize(frame, width=920)
            (H, W) = frame.shape[:2]
            
            if initBB is None:
                initBB = cv2.selectROIs("Frame", frame, fromCenter=False,
                                           showCrosshair=True)
                
                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                tracker1.init(frame, tuple(initBB[0,:]))
                tracker2.init(frame, tuple(initBB[1,:]))
                tracker3.init(frame, tuple(initBB[2,:]))
                tracker4.init(frame, tuple(initBB[3,:]))
                
                fps = FPS().start()
            
            # check to see if we are currently tracking an object
            if initBB is not None:
                # grab the new bounding box coordinates of the object
                (success, box1) = tracker1.update(frame)
                (success, box2) = tracker2.update(frame)
                (success, box3) = tracker3.update(frame)
                (success, box4) = tracker4.update(frame)
                # check to see if the tracking was a success
                if success:
                    (x1, y1, w1, h1) = [int(v) for v in box1]
                    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1),
                                  (0, 255, 0), 2)
                    (x2, y2, w2, h2) = [int(v) for v in box2]
                    cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2),
                                  (0, 255, 0), 2)
                    (x3, y3, w3, h3) = [int(v) for v in box3]
                    cv2.rectangle(frame, (x3, y3), (x3 + w3, y3 + h3),
                                  (0, 255, 0), 2)
                    (x4, y4, w4, h4) = [int(v) for v in box4]
                    cv2.rectangle(frame, (x4, y4), (x4 + w4, y4 + h4),
                                  (0, 255, 0), 2)
                    if cnt == 1:
                        centerInit = np.float32([[int(x1+w1/2),int(y1+h1/2)],[int(x2+w2/2),int(y2+h2/2)],
                                                 [int(x3+w3/2),int(y3+h3/2)],[int(x4+w4/2),int(y4+h4/2)]])
                        out.write(frame)
                        cnt += 1
                    else:
                        center = np.float32([[int(x1+w1/2),int(y1+h1/2)],[int(x2+w2/2),int(y2+h2/2)],
                                   [int(x3+w3/2),int(y3+h3/2)],[int(x4+w4/2),int(y4+h4/2)]])
                        projective_matrix = cv2.getPerspectiveTransform(center,centerInit)
                        img_output = cv2.warpPerspective(frame, projective_matrix,(W,H) )
    
                        out.write(img_output)
                        cnt += 1

                # If the number of time is not sufficient there will be a division
                # by zero in the computation of the number of fps 
                cv2.imshow("Frame", frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        ret, frame = vs.read()
        
    out.release()
    vs.release()
    cv2.destroyAllWindows()