import cv2
import numpy as np
import math
import os

def calibrationCamera(filename, videoFileName, boardDim, sizeSquare, nbrImageExtract):
    
    vid = cv2.VideoCapture(videoFileName)
    W  = vid.get(cv2.CAP_PROP_FRAME_WIDTH)   
    H = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fps =  round(vid.get(cv2.CAP_PROP_FPS))
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = fps//2
    # Defining the dimensions of checkerboard
    CHECKERBOARD = (boardDim[0],boardDim[1])
    # Criteria to stop computation
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = [] 
    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    #objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0]*sizeSquare:40, 0:CHECKERBOARD[1]*sizeSquare:40].T.reshape(-1, 2)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0]*sizeSquare:sizeSquare, 0:CHECKERBOARD[1]*sizeSquare:sizeSquare].T.reshape(-1, 2)
    # Path("imagesWorks").mkdir(parents=True, exist_ok=True)
    i = 0
    interval = frame_count//nbrImageExtract
    nbFrame = 0
    while(vid.isOpened()):
        
        ret1, frame = vid.read()
        if ret1 is True and nbFrame >= interval*i:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # Transforming gray image into binary one using algorithm Otsu to find the threshold
            (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # Find the chess board corners. If desired number of corners are found in the image then ret = true
            ret2, corners = cv2.findChessboardCorners(im_bw, CHECKERBOARD,None)
            
            # If desired number of corner are detected, we refine the pixel coordinates and display them on the images of checker board
            if ret2 == True:
                objpoints.append(objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(im_bw, corners, (11,11),(-1,-1), criteria)
                
                imgpoints.append(corners2)
                i += 1
            img = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret1)
            cv2.imwrite('testCalib'+str(i)+'.jpg', img)
        elif ret1 is not True:
            break
        nbFrame += 1
    vid.release()
    
    ## Find calibration parameters of camera
    
    ret, mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    ## Compute FOV horizontal and vertical 
    
    fx = mtx[0][0]
    fy = mtx[1][1]
    
    fovx = 2 * math.atan(W / (2 * fx)) * 180.0 / math.pi
    fovy = 2 * math.atan(H / (2 * fy)) * 180.0 / math.pi
    fovdiag = 2 * math.atan(np.sqrt(H**2 + W**2) / (2 * fx)) * 180.0 / math.pi
    
    ## Compute mean of reprojection error
    
    tot_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, distCoeffs)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        tot_error += error
    meanError = tot_error/len(objpoints)
    
    ## Save
    
    data = {'ret': ret,
         'mtx': mtx,
         'distCoeffs': distCoeffs,                   
         'rvecs': rvecs,                   
         'tvecs': tvecs,                   
         'FOVx': fovx,
         'FOVy': fovy,
         'FOVdiag':fovdiag,
         'meanError':meanError}
    np.save(filename+'.npy',data)
    
def knownCalibrationParam(filename, distCoeffs, cx, cy, fovx, fovy, fovdiag):
    mtx=np.float32([[fovx, 0, cx], 
                 [0, fovy, cy], 
                 [0, 0, 1]])
    data = {'mtx': mtx,
         'distCoeffs': distCoeffs,                                     
         'FOVx': fovx,
         'FOVy': fovy,
         'FOVdiag':fovdiag}    
    np.save(filename+'.npy',data)

def applyCalibrationOnVideoFrames(filepath, videoRange, calibrationFile):
    # Here we only take into account the video range to gain some time we don't take 
    # the step since it will be done in the PIV analysis ste
    calibParam = np.load(calibrationFile, allow_pickle = 'TRUE').item()
    distCoeffs = calibParam['distCoeffs']
    mtx = calibParam['mtx']
    
    base=os.path.basename(filepath)
    
    names = os.path.splitext(base)
    
    nameUndistortedVideo = 'Video/' + names[0] + 'Undistorted' + '.mp4'
    
    vs = cv2.VideoCapture(filepath)
    ret, frame = vs.read()
    (H, W) = frame.shape[:2]
    fps =  round(vs.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(nameUndistortedVideo, fourcc, fps, (W,H),0)
    nbFrame = 1
    while vs.isOpened():
        if ret is True and videoRange[0]*fps <= nbFrame:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_output = cv2.undistort(frame, mtx, distCoeffs, None, mtx)
            out.write(img_output)
        nbFrame += 1
        ret, frame = vs.read()
        if videoRange[1]*fps <= nbFrame:
            break
    out.release()
    vs.release()
    return nameUndistortedVideo
