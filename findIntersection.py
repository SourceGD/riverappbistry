import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def interpolated_intercepts(x, y1, y2):
    """Find the intercepts of two curves, given by the same x data"""

    def intercept(point1, point2, point3, point4):
        """find the intersection between two lines
        the first line is defined by the line between point1 and point2
        the first line is defined by the line between point3 and point4
        each point is an (x,y) tuple.

        So, for example, you can find the intersection between
        intercept((0,0), (1,1), (0,1), (1,0)) = (0.5, 0.5)

        Returns: the intercept, in (x,y) format
        """    

        
        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C

        def intersection(L1, L2, x, y):
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if(D!=0):
                x = Dx / D
                y = Dy / D
            return x,y

        L1 = line([point1[0],point1[1]], [point2[0],point2[1]])
        L2 = line([point3[0],point3[1]], [point4[0],point4[1]])
        x = [point3[0][0]]
        y = [point3[1][0]]
        R = intersection(L1, L2, x, y)

        return R

    idxs = np.argwhere(np.diff(np.sign(y1 - y2)) != 0)

    xcs = []
    ycs = []

    for idx in idxs:
        xc, yc = intercept((x[idx], y1[idx]),((x[idx+1], y1[idx+1])), ((x[idx], y2[idx])), ((x[idx+1], y2[idx+1])))
        xcs.append(xc)
        ycs.append(yc)
    return np.array(xcs), np.array(ycs)

def findWaterLevel(filename,L):
    dem = np.loadtxt(filename , delimiter = ',')
    x = np.array(dem[:,0])
    y1 = np.array(dem[:,1])
    H = max(y1)
    Hmin = min(y1)
    n = 1000
    deltaH = (H-Hmin)/n
    deltaX = float('inf')
    while abs(deltaX-L) > 1e-3:
        if H>=Hmin:
            y2 = np.array([H]*len(x))    
            xcs, ycs = interpolated_intercepts(x,y1,y2)
            if len(xcs)==2:
                deltaX = xcs[1]-xcs[0]
            H = H-deltaH
        else:
            xcs = np.asarray([[-100000],[-1000000]])
            ycs=xcs
            break 
    return(ycs[0],xcs,ycs)
    # return(ycs[0]-Hmin,xcs,ycs)
    
def findLength(filename, WL):
    dem = np.loadtxt(filename , delimiter = ',')
    x = np.array(dem[:,0])
    y = np.array(dem[:,1])
    
    count = 0
    interp1 = []
    interp2 = []
    L = 0
    xL = [0,0]
    for k in range(len(y)-1):
        if y[k]>= WL and y[k+1]<= WL:
            interp1 = [x[k], x[k+1],y[k], y[k+1]]
            count =+ 1
        if y[k]<= WL and y[k+1] >= WL:
            interp2 = [x[k], x[k+1], y[k], y[k+1]]
            count += 1
            
    if count != 2:
        raise NameError('The water level have more than 2 interceptions with the bathymetry')
    else:
        f1 = interp1d(interp1[2:], interp1[:2])
        f2 = interp1d(interp2[2:], interp2[:2])
        xL[0] = f1(WL)
        xL[1] = f2(WL)
        
    L=xL[1]-xL[0]
    return L



