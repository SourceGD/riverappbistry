import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def filtersImage(img, choice, *args):
    
    """ Different filters choices and application on the images """
    
    if choice == 'CLAHE':
        clahe = cv2.createCLAHE(clipLimit=args[0], tileGridSize=args[1])
        return clahe.apply(img) 
        
    elif choice == 'Intensity Capping':
        img_flatten = img.flatten()
        img_flatten = np.ma.masked_where(img_flatten > args[0], img_flatten)
        img_flatten = np.ma.filled(img_flatten,args[0]).astype('uint8')
        return img_flatten.reshape(img.shape)
        
    elif choice == 'Intensity high-pass':
        blur = cv2.GaussianBlur(img,args[1],args[2],args[3])
        img2 = cv2.subtract(img,blur)
        img_flatten = img2.flatten()
        img_flatten = (img_flatten*args[0]).astype('uint8')
        return img_flatten.reshape(img.shape)
        
    elif choice == 'Mean Denoising':
        return cv2.fastNlMeansDenoising(img, args[0], args[1], args[2])
        
    elif choice == 'Contrast/Brightness':
        return cv2.convertScaleAbs(img, alpha=args[0], beta=args[1])
        
    elif choice == 'Gamma correction':
        lookUpTable = np.array(np.clip(pow(np.array(range(256))/ 255.0, args[0]) * 255.0, 0, 255), np.uint8)
        return cv2.LUT(img, lookUpTable)
    
    return None
        
def applyFilterOnVideoFrames(filepath, videoRange, filters, parametersFilters):
    # Here we only take into account the video range to gain some time we don't take 
    # the step since it will be done in the PIV analysis step
    base=os.path.basename(filepath)
    
    names = os.path.splitext(base)
    
    nameFilteredVideo = 'mov/' + names[0] + 'Filtered' + '.mp4'
    
    vs = cv2.VideoCapture(filepath)
    ret, frame = vs.read()
    (H, W) = frame.shape[:2]
    fps =  round(vs.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(nameFilteredVideo, fourcc, fps, (W,H),0)
    nbFrame = 1
    while vs.isOpened():
        if ret is True and videoRange[0]*fps <= nbFrame:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_output = frame.copy()  
            for i in range(len(filters)):
                img_output = filtersImage(img_output, filters[i], *parametersFilters[i])
            out.write(img_output)
        nbFrame += 1
        ret, frame = vs.read()
        if videoRange[1]*fps <= nbFrame:
            break
    out.release()
    vs.release()
    return nameFilteredVideo
    