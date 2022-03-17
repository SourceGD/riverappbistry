import numpy as np
import cv2 

def computeMeanVelocity(frame):

    velocity_data = np.load('velocity.npy', allow_pickle = 'TRUE').item()
    maskandroi = np.load('maskandroi.npy', allow_pickle = 'TRUE').item()
   
    Mask = ~maskandroi['mask']
    mask = np.array(Mask, dtype= np.int32)*255
    mask = mask.astype(np.uint8)
    frame = cv2.bitwise_and(frame, frame, mask = mask)
    
    x = velocity_data[0]['x']
    y = velocity_data[0]['y']
    #y = abs(y-frame.shape[0])   #ligne qui créait nos triangles sans vitesses avec l'ortho (elle inverse le mask)
    nb_rows = x.shape[0]
    nb_cols = x.shape[1]
    
    nb = max(velocity_data.keys())
    
    #print('nb dans mean velocity vaut ', nb )

    u_mean = np.array([[0]*nb_cols]*nb_rows, dtype = np.float64)
    v_mean = np.array([[0]*nb_cols]*nb_rows, dtype = np.float64)
    mask_out = np.zeros(x.shape[:2]).astype(bool)
    
    
    xpix = x.astype(np.int32)
    ypix = y.astype(np.int32)
    
    
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if Mask[ypix[i][j]][xpix[i][j]]:
                mask_out[i][j] = True
    
    for i in range(nb):
        u_mean[mask_out] += velocity_data[i]['u'][mask_out]
        v_mean[mask_out] += velocity_data[i]['v'][mask_out]

        
    u_mean = u_mean/(nb+1)
    v_mean = v_mean/(nb+1)
    
    
    return (x, y, u_mean, v_mean)
   