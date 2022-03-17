import cv2
import numpy as np
import math
from scipy import ndimage

def orthorectificationComputation(img, L, pts_src, pts_mask, scaling_factor):
    
    ## Distances between the fours points of reference ABCD (A top left corner then clockwise order)
    ##  in the following order [L_AB, L_BC, L_CD, L_DA, L_AC, L_DB]
    # L = [10.3, 16.5, 7.1, 9.2, 11.9, 18]      # image from tuto river
    
    # Points coordinates computation 
    # We consider first that P1 and P4 are vertically aligned and P4 as the  origin
    P1, P4 = [0,L[3]], [0,0]
    # Then we compute other coordinates using cosine law
    alpha = math.acos((L[3]**2+L[5]**2-L[0]**2)/(2*L[3]*L[5]))
    P2 = [L[5]*math.sin(alpha),L[5]*math.cos(alpha)]
    beta = math.acos((L[3]**2+L[2]**2-L[4]**2)/(2*L[3]*L[2]))
    P3 = [L[2]*math.sin(beta),L[2]*math.cos(beta)]
    
    # Then we put all coordinates in X and Y vectors
    X = np.array([P1[0],P2[0],P3[0],P4[0]])
    Y = np.array([P1[1],P2[1],P3[1],P4[1]])
    
    # Since cv2 origin is top left and negative coordinate are not wanted (pixel not negative) 
    # we need to shift coordinates and make P1 the origin
    if min(X) < 0:
        X = X - min(X)
    if min(Y) < 0:
        Y = Y - min(Y)
    Y = abs(Y - max(Y))
    
    # the pts of destination, pts_dst, of the transformation are the real coordinates computed
    # but since we want to show them on image we need to scale these coordinates by a 
    # scaling factor and converted them to integer as they represent pixelpts_dst = list(zip(X,Y))
    #scaling_factor = 30

    pts_dst = (np.array(list(zip(X,Y)))*scaling_factor).astype(np.int32)

    # we need to crop the image to only display mask selected region
    Xmin, Ymin = min(pts_mask[:,0]), min(pts_mask[:,1])
    Xmax, Ymax = max(pts_mask[:,0]), max(pts_mask[:,1])
    
    img = img[int(Ymin):int(Ymax), 
              int(Xmin):int(Xmax)]
    # since we crop the image we need to shift pixel coordinates of the mask and 
    # of the 4 points in the original image
    pts_mask[:,0] -= Xmin
    pts_mask[:,1] -= Ymin
    
    pts_src[:,0] -= Xmin
    pts_src[:,1] -= Ymin
    
    # we fill the region outside the mask with black pixels
    (H, W) = img.shape[:2]
    mask = np.zeros((H,W))
    white = (255, 255, 255)
    cv2.fillPoly(mask, [pts_mask], white)
    mask = mask.astype(np.uint8)
    img_masked = cv2.bitwise_and(img, mask)
    # cv2.imshow("Image Masked", img_masked)
    
    ## Compute homography matrix
    
    h1, _ = cv2.findHomography(pts_src, pts_dst)
    
    # But for the moment the point P1 will be at the origin of the orthorectified image
    # so we will not see all the selected region (since some points will be in negative coordinates)
    # Then we need to compute the value of the mask points in the transformed image
    # and after shift pts_dst by the minimum values
    pts_mask_after = cv2.perspectiveTransform(np.array([pts_mask.tolist()], dtype=np.float32), h1)
    
    Xmin_after, Ymin_after = pts_mask_after[0][:,0].min(), pts_mask_after[0][:,1].min()
    Xmax_after, Ymax_after = pts_mask_after[0][:,0].max(), pts_mask_after[0][:,1].max()
    
    if Xmin_after < 0:
        pts_dst[:,0] = pts_dst[:,0] + abs(Xmin_after)
    else:
        pts_dst[:,0] = pts_dst[:,0] - abs(Xmin_after)
    if Ymin_after < 0:
        pts_dst[:,1] = pts_dst[:,1] + abs(Ymin_after)
    else:
        pts_dst[:,1] = pts_dst[:,1] - abs(Ymin_after)
    
    
    ## Computation of final homography matrix
    h2, _ = cv2.findHomography(pts_src, pts_dst)
    
    img_rectified = cv2.warpPerspective(img_masked, h2, (int(Xmax_after-Xmin_after),int(Ymax_after-Ymin_after)))
    # Display images
    # cv2.imshow("Image Rectified", img_rectified)
    return img_masked, img_rectified, h2, Xmin, Ymin#, scaling_factor


def rotation(img_rectified, pts_align):
    # Rotation of the orthorectified image

    angle_rotation = math.atan((pts_align[1][1]-pts_align[0][1])/(pts_align[1][0]-pts_align[0][0]))
    angle_rotation_degree = angle_rotation*180/math.pi
    
    img_rotated = ndimage.rotate(img_rectified, angle_rotation_degree, reshape=False)
    
    return img_rotated, angle_rotation

def selectionSection(pts_section, angle_rotation, h2, Xmin, Ymin):

    _, h2_inv = cv2.invert(h2)
    pts_sectionOrg = cv2.perspectiveTransform( np.array([list(pts_section)],dtype = np.float64),
                                                 h2_inv)
    
    # Check if selected region is also in the ROI of the PIV analysis
    maskandroi = np.load('maskandroi.npy', allow_pickle = 'TRUE').item()
    ROI = maskandroi['ROI']
    pts_sectionOrg[0][:,0] += Xmin
    pts_sectionOrg[0][:,1] += Ymin
    inside_roi = True
    if ~np.all((pts_sectionOrg[0][:,0] > ROI[2]) &
               (pts_sectionOrg[0][:,0] < ROI[3]) &
               (pts_sectionOrg[0][:,1] > ROI[0]) &
               (pts_sectionOrg[0][:,1] < ROI[1])
               ):
        print('Section choosen must be in the ROI selected for the PIV analysis')
        inside_roi = False
    
    return pts_sectionOrg[0], inside_roi
   











