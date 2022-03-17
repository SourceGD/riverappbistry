import cv2
import numpy as np
import math
from findIntersection import *

def retrieveSectionInformation(x, y, u_mean, v_mean, ROI, img_rectified, img_rotated,
                                pts_sectionRot, Xmin, Ymin, h, angle, nbSubSection):
    
    # We need to shift the grid coordinates of ROI where PIV analysis was performed
    # to the coordinates pixel of the img 
    x_loc = x + (ROI[2])
    y_loc = y + (ROI[0])
    
    # We reshape the 4 arrays of x, y, u_mean, v_mean into 2 arrays one containing
    # the coordinates of the grid and the other the velocity component
    # We reshape then to simplify further operations
    n = x_loc.shape[0]*x_loc.shape[1]
    grid_points = np.array([list(zip(x_loc.reshape(1,n)[0],y_loc.reshape(1,n)[0]))])
    velocity = np.array([list(zip(u_mean.reshape(1,n)[0],v_mean.reshape(1,n)[0]))])    
    # The homography matrix was computed using a crop image in order to be 
    # in the same conditions we need to shift grid points as well using 
    grid_points[0][:,0] -= Xmin
    grid_points[0][:,1] -= Ymin
    # Then we simpy apply the homography matrix
    gridOrtho = cv2.perspectiveTransform(grid_points, h)
    # The v velocity component should be negative since y axis on image are inversed
    # but openPIV in order to simplify the display by quiver return v positive
    # so before going any further we need to make it negative again 
    # and add angles='xy' in quiver when we want to display it to indicate quiver
    # that the axis is inversed in this case
    velocity[0][:,1] = -velocity[0][:,1] 
    # Then for the velocity  orthorectification we first add the velocity to 
    # the grid coordinates (since we cannot do it on (u,v) values alone)
    velOrtho = cv2.perspectiveTransform(grid_points+velocity, h)
    # Then since we are only intersted in the velocity value we substract the 
    # orthorectfied grid points values
    velOrtho = velOrtho - gridOrtho    
    """ Rotate results """
    # Because there is a rotation we need to translate to the origin, then rotate,
    # then translate back. We can take the center of the image as origin.
    org_imgCenter = (np.array(img_rectified.shape[:2][::-1])-1)/2
    rot_imgCenter = (np.array(img_rotated.shape[:2][::-1])-1)/2
    
    # Translate (only need to do it for grid since velocity components add to the 
    # grid coordinates)
    gridOrtho -= org_imgCenter
    xgrid, ygrid = gridOrtho[0][:,0], gridOrtho[0][:,1]
    xvel, yvel = velOrtho[0][:,0], velOrtho[0][:,1]
    # rotate
    gridOrtho[0][:,0] = math.cos(angle)*xgrid + math.sin(angle)*ygrid
    gridOrtho[0][:,1] = -math.sin(angle)*xgrid + math.cos(angle)*ygrid
    
    velOrtho[0][:,0] = math.cos(angle)*xvel + math.sin(angle)*yvel
    velOrtho[0][:,1] = -math.sin(angle)*xvel + math.cos(angle)*yvel
    # Translate back (only need to do it for grid since velocity components add to the 
    # grid coordinates)
    gridOrtho += rot_imgCenter
    
    """ Retrieve closet velocity vectors from section choosen """
    
    # Since the section choosen is horizontal in the rotated and orthorectified
    # image the distance to considered bewteen grid points and pts_section is only vertical
    distance = abs(gridOrtho[0][:,1]-pts_sectionRot[0][1])
    # Again we flatten the gird orthorectifed and rotated array as well as the
    # velociy one
    xgrid_rot, ygrid_rot = np.array(gridOrtho[0][:,0].tolist()), np.array(gridOrtho[0][:,1].tolist())
    u_meanflat, v_meanflat = np.array(velOrtho[0][:,0].tolist()), np.array(velOrtho[0][:,1].tolist())
    # we compute the delta needed for the number of subsection wanted
    len_line = abs(pts_sectionRot[1][0]-pts_sectionRot[0][0])
    deltaX = len_line/nbSubSection
    indices = np.array(range(int(nbSubSection+1)))
    # We compute the x position of the point on the section
    xpos = (deltaX)*indices + pts_sectionRot[0][0]
    
    # Initialization of the arrays that will store the closest vector of each 
    # subsections
    x_interest, y_interest = np.array([]), np.array([])
    u_interest, v_interest = np.array([]), np.array([])
    
    for i in range(nbSubSection):
        # we find the index of points that are in the same x region that the subsection
        ind = [(xgrid_rot>=xpos[i])
               & (xgrid_rot<=xpos[i+1])]
        # Then we find the minimal distance within all these points
        indmin = distance[(xgrid_rot>=xpos[i])
                          & (xgrid_rot<=xpos[i+1])].argmin()
        # Finally we store the vetors of interest
        x_interest = np.append(x_interest,(xgrid_rot[ind[0]])[indmin])
        y_interest = np.append(y_interest,(ygrid_rot[ind[0]])[indmin])
        u_interest = np.append(u_interest,(u_meanflat[ind[0]])[indmin])
        v_interest = np.append(v_interest,(v_meanflat[ind[0]])[indmin])
        
    return x_interest, y_interest, u_interest, v_interest

def retrieveSectionInformationWithoutOrtho(x, y, u_mean, v_mean, ROI, img,
                               pts_sectionRot, nbSubSection,img_rotated, angle):
    
    # We need to shift the grid coordinates of ROI where PIV analysis was performed
    # to the coordinates pixel of the img 
    #x += (ROI[2])
    #y += (ROI[0])
    # ici 2 lignes mises en commentaires car décalage des flèches de vecteurs vitesses
    # We reshape the 4 arrays of x, y, u_mean, v_mean into 2 arrays one containing
    # the coordinates of the grid and the other the velocity component
    # We reshape then to simplify further operations
    n = x.shape[0]*x.shape[1]
    grid_points = np.array([list(zip(x.reshape(1,n)[0],y.reshape(1,n)[0]))])
    velocity = np.array([list(zip(u_mean.reshape(1,n)[0],v_mean.reshape(1,n)[0]))])    
    # The v velocity component should be negative since y axis on image are inversed
    # but openPIV in order to simplify the display by quiver return v positive
    # so before going any further we need to make it negative again 
    # and add angles='xy' in quiver when we want to display it to indicate quiver
    # that the axis is inversed in this case
    velocity[0][:,1] = -velocity[0][:,1] 
    
    
    """ Rotate results """
    # Because there is a rotation we need to translate to the origin, then rotate,
    # then translate back. We can take the center of the image as origin.
    org_imgCenter = (np.array(img.shape[:2][::-1])-1)/2
    rot_imgCenter = (np.array(img_rotated.shape[:2][::-1])-1)/2
    
    # Translate (only need to do it for grid since velocity components add to the 
    # grid coordinates)
    grid_points -= org_imgCenter
    xgrid, ygrid = grid_points[0][:,0], grid_points[0][:,1]
    xvel, yvel = velocity[0][:,0], velocity[0][:,1]
    # rotate
    grid_points[0][:,0] = math.cos(angle)*xgrid + math.sin(angle)*ygrid
    grid_points[0][:,1] = -math.sin(angle)*xgrid + math.cos(angle)*ygrid
    
    velocity[0][:,0] = math.cos(angle)*xvel + math.sin(angle)*yvel
    velocity[0][:,1] = -math.sin(angle)*xvel + math.cos(angle)*yvel
    # Translate back (only need to do it for grid since velocity components add to the 
    # grid coordinates)
    grid_points += rot_imgCenter
    
    """ Retrieve closet velocity vectors from section choosen """
    u_mean, v_mean = np.array(velocity[0][:,0].tolist()), np.array(velocity[0][:,1].tolist())
    # Since the section choosen is horizontal in the rotated and orthorectified
    # image the distance to considered bewteen grid points and pts_section is only vertical
    distance = abs(grid_points[0][:,1]-pts_sectionRot[0][1])
    # Again we flatten the gird orthorectifed and rotated array as well as the
    # velociy one
    xgrid, ygrid = np.array(grid_points[0][:,0].tolist()), np.array(grid_points[0][:,1].tolist())
    # we compute the delta needed for the number of subsection wanted
    len_line = abs(pts_sectionRot[1][0]-pts_sectionRot[0][0])
    deltaX = len_line/nbSubSection
    indices = np.array(range(int(nbSubSection+1)))
    # We compute the x position of the point on the section
    xpos = (deltaX)*indices + pts_sectionRot[0][0]
    
    # Initialization of the arrays that will store the closest vector of each 
    # subsections
    x_interest, y_interest = np.array([]), np.array([])
    u_interest, v_interest = np.array([]), np.array([])
    
    for i in range(nbSubSection):
        # we find the index of points that are in the same x region that the subsection
        ind = [(xgrid>=xpos[i])
               & (xgrid<=xpos[i+1])]
        # Then we find the minimal distance within all these points
        indmin = distance[(xgrid>=xpos[i])
                          & (xgrid<=xpos[i+1])].argmin()
        # Finally we store the vetors of interest
        x_interest = np.append(x_interest,(xgrid[ind[0]])[indmin])
        y_interest = np.append(y_interest,(ygrid[ind[0]])[indmin])
        u_interest = np.append(u_interest,(u_mean[ind[0]])[indmin])
        v_interest = np.append(v_interest,(v_mean[ind[0]])[indmin])
    
    return x_interest, y_interest, u_interest, v_interest

def computeAreaSection(x, y, level_water, nbSubSect):
    
    line_water = np.array([level_water]*len(y))
    xi, yi = interpolated_intercepts(np.array(x),np.array(y),line_water)
    ## AREA COMPUTATION 
    # First we add the intersection points with the water level and the subsection points as well
    delta = (xi[1][0] - xi[0][0])/nbSubSect
    x_SubSect = xi[0][0] + delta*np.array(range(nbSubSect+1))
    y_SubSect = np.concatenate((yi[0], np.interp(x_SubSect[1:-1],x,y) , yi[1]))
    x,y = np.concatenate((xi[:,0],x,x_SubSect)), np.concatenate((yi[:,0],y,y_SubSect))
    ind = np.argsort(x)
    x, y = x[ind], y[ind]
    # Then we isolate the points within the intersection ones
    ind = (    (np.round(x,5) >= round(xi[0][0],5)) 
            &  (np.round(x,5) <= round(xi[1][0],5)) )
    x, y = x[ind], y[ind]
    area = np.array([])
    x_area = []
    y_area = []
    for i in range(nbSubSect):
        ind = (    (np.round(x,5) >= round(x_SubSect[i],5)) 
                &  (np.round(x,5) <= round(x_SubSect[i+1],5)) )
        # Since trapz computes area bellow the points we give it we must substract
        # the area compute by trapz to the rectangle area of the subsection to 
        # have the area we are looking for
        areaSub = yi[0]*(x[ind][-1] - x[ind][0]) - np.trapz(y[ind],x[ind])
        area = np.append(area,areaSub)
        x_area += [[x[ind][0]] + x[ind].tolist() + [x[ind][-1]]] 
        y_area += [[yi[0][0]] + y[ind].tolist() + [yi[0][0]] ]
    
    return area, x_area, y_area

        
    
def computeDischarge(velocity, coefficient, area, scaling_factor):
    # In the orthorectification part we have put the v velocity negative 
    # now we must put it positive 
    velocity = - velocity
    velocity = velocity/scaling_factor
    return abs(sum(velocity*coefficient*area))