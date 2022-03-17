import matplotlib.pyplot as plt
import numpy as np   
import matplotlib.image as mpimg
import math
import cv2
from scipy import optimize

""" Undistort frames works only when images used for calibration and images use for 
    this computation are the same format (video frame in both cases or picture 
    in both cases). Morover calibration must be performed or results loaded
    before using this method since it needs the FOVs compute at this step. """

def droneGeometryWaterLevel(filename, pathImgClose, pathImgFar, deltaH):
    
    img_close = mpimg.imread(pathImgClose)
    img_far = mpimg.imread(pathImgFar)
    if filename != '':
        # Load 
        calibParam = np.load(filename, allow_pickle = 'TRUE').item()
        distCoeffs = calibParam['distCoeffs']
        FOVx = calibParam['FOVx']
        FOVy = calibParam['FOVy']
        FOVdiag = calibParam['FOVdiag']
        mtx = calibParam['mtx']
        img_far = cv2.undistort(img_far, mtx, distCoeffs, None, mtx)
        img_close = cv2.undistort(img_close, mtx, distCoeffs, None, mtx)
    
    H,W,_ = img_close.shape
    
    """ Length of river in pixel in the 2 images """
    
    # First image
    plt.figure()
    plt.imshow(img_close)
    dataClose = plt.ginput(2)
    LenPixClose = np.sqrt((dataClose[1][0] - dataClose[0][0])**2 + (dataClose[1][1] - dataClose[0][1])**2)
    # Second image
    plt.figure()
    plt.imshow(img_far)
    dataFar = plt.ginput(2)
    LenPixFar = np.sqrt((dataFar[1][0] - dataFar[0][0])**2 + (dataFar[1][1] - dataFar[0][1])**2)
    # Close the image
    plt.close('all')
    
    """ Computation of several parameters depending on the orientation of the river 
        section on the image """    
    
    MiddlePointRiver = np.array([[(dataClose[1][0] + dataClose[0][0])/2,(dataClose[1][1] + dataClose[0][1])/2],
                             [(dataFar[1][0] + dataFar[0][0])/2,(dataFar[1][1] + dataFar[0][1])/2]])
    MiddlePointImg = np.array([W/2,H/2])
    orientationRiverSection = np.array([np.arctan((dataClose[1][1] - dataClose[0][1])/(dataClose[1][0] - dataClose[0][0]))*180/np.pi,
                                        np.arctan((dataFar[1][1] - dataFar[0][1])/(dataFar[1][0] - dataFar[0][0]))*180/np.pi])
    # Set the first threshold value to -1e-3 because if set to 0 the case where the angle is 0 is problematic
    thresholds = np.array([-1e-3,30,60])
    FOVChoices = np.array([FOVx, FOVy, FOVdiag])
    ImgLenPixChoices = np.array([W, H, np.sqrt(W**2 + H**2)])
    ImgLenPixStartPointChoices = np.array([[0,H/2], [W/2,0], [0,0]])
    ImgLenPixEndPointChoices = np.array([[W,H/2], [W/2,H], [W,H]])
    
    # Initialization of the different arrays 
    FOV, ImgLenPix, deltaX = (np.array([0,0]) for i in range(3))
    ImgLenPixStartPoint, ImgLenPixEndPoint, n, ProjectionPoints = (np.array([[0,0],[0,0]]) for i in range(4))
    
    for i in range(2):
        ind = abs(orientationRiverSection[i]) > thresholds
        FOV[i] = FOVChoices[ind][-1]
        ImgLenPix[i] = ImgLenPixChoices[ind][-1]
        ImgLenPixStartPoint[i] = ImgLenPixStartPointChoices[ind][-1]
        ImgLenPixEndPoint[i] = ImgLenPixEndPointChoices[ind][-1]
        n[i] = ImgLenPixEndPoint[i] - ImgLenPixStartPoint[i]
        n[i]= n[i]/np.linalg.norm(n[i], 2)
        ProjectionPoints[i] = ImgLenPixStartPoint[i] + n[i]*np.dot(MiddlePointRiver[i] - ImgLenPixStartPoint[i], n[i])
        factor = np.sign((MiddlePointRiver[i][0]-ProjectionPoints[i][0]) + (MiddlePointRiver[i][1]-ProjectionPoints[i][1]))
        deltaX[i] = factor*(np.sqrt((MiddlePointImg[0]-ProjectionPoints[i][0])**2 + (MiddlePointImg[1]-ProjectionPoints[i][1])**2))/ImgLenPix[i]
    
    print(deltaX)    
    """ Angle of view  """
    #old formulas
    #alphaClose = (FOV[0]*LenPixClose/ImgLenPix[0])*(np.pi/180) 
    #alphaFar = (FOV[1]*LenPixFar/ImgLenPix[0])*(np.pi/180)
    
    """ Solve system """
        
    ## Easy one:
        
    """ Angle of view center-drone case """  

    alphaCloseCenter = 2*np.arctan(math.tan(FOV[0]/2*(np.pi/180))*LenPixClose/ImgLenPix[0])
    alphaFarCenter = 2*np.arctan(math.tan(FOV[1]/2*(np.pi/180))*LenPixFar/ImgLenPix[1])
   
    a = np.array([[1.0/2.0,-math.tan(alphaFarCenter/2.0)], [1.0/2.0,-math.tan(alphaCloseCenter/2.0)]])
    b = np.array([deltaH*math.tan(alphaFarCenter/2.0),0])
    x = np.linalg.solve(a, b)
    L1 = x[0]
    H1 = x[1]
    
    
    ## Complex one:
    
    """ Angle of view off center-drone case """  

    alphaClose = np.arctan(((LenPixClose/2-deltaX[0])/ImgLenPix[0])*2*math.tan(FOV[0]/2*(np.pi/180))) +\
                  np.arctan(((LenPixClose/2+deltaX[0])/ImgLenPix[0])*2*math.tan(FOV[0]/2*(np.pi/180)))  
    
    alphaFar = np.arctan(((LenPixClose/2-deltaX[1])/ImgLenPix[1])*2*math.tan(FOV[1]/2*(np.pi/180))) +\
                  np.arctan(((LenPixClose/2+deltaX[1])/ImgLenPix[1])*2*math.tan(FOV[1]/2*(np.pi/180)))
     
            
    def funComplex(x):
        return [math.tan(x[2]) - (x[1]+deltaH)/(x[0]*(1/2 - deltaX[1])),
                math.tan(x[3]) - x[1]/(x[0]*(1/2 - deltaX[0])),
                math.tan(x[4]) - (x[1]+deltaH)/(x[0]*(1/2 + deltaX[1])),
                math.tan(x[5]) - x[1]/(x[0]*(1/2 + deltaX[0])),
                alphaFar + x[2] + x[4] - math.pi,
                alphaClose + x[3] + x[5] - math.pi,
               ]
    sol = optimize.root(funComplex, [L1, H1 ,(math.pi-alphaFar)/2,
                                      (math.pi-alphaClose)/2,(math.pi-alphaFar)/2,(math.pi-alphaClose)/2], method='hybr')
    L2,H2,_,_,_,_ = sol.x
    
    # Check to see if second method has failed or not if it has failed 
    # return first result
    if abs(L1-L2)/max(L1,L2) > 0.5 and abs(H1-H2)/max(H1,H2) > 0.5:
        return L1,H1
    else:
        return L2,H2
