## 1. IMPORT PACKAGES FILE

from packagesFile import *

## 2. GLOBAL SETTINGS

Config.set('input', 'mouse', 'mouse,disable_multitouch') # Disable multi-touch emulation when right click with mouse
plt.figure()  # Call to plt.figure() just to avoid future calls of plt.figure() to change the window size
Window.size = 1040, 715 # Window size initialization

## 3. CODE

class FileNotFound(Popup):
    
    """Screen that loads the popup when no file is selected"""
    
    pass

class ValueNotFound(Popup):
    
    """Screen that loads the popup when no value is writen"""
    pass

## 3.1 BATHYMETRY SCREENS

class Bathymetry(Screen):
    
    """Screen that proposes the choice for the retrievement of the bathymetry data """    
    pass

class BathymetryCreate(Screen):
    
    """Screen that proposes the choice for the creation of the bathymetry data """
    pass
            
class BathymetryLoad(Screen):
    
    """ Screen that plots the bathymetry file selected """
    
    def on_enter(self):
        # Firstly we need to clear the previous plot in case the user presses 
        # the button "Go back" to avoid having mutliple graphs
        self.ids.LoadBathGraphID.clear_widgets()
        # To access to the global variables of the app such as the name
        # of the bathymetry file we first need to get the current status of the app
        app = App.get_running_app()
        # Loading of the bathymetry data
        data = np.loadtxt(app.BATHFILEPATH, delimiter = ',')

        X = data[:,0]
        Y = data[:,1]
        # Plotting and color/style settings
        fig = plt.figure()
        plt.plot(X,Y)
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.rc('grid', linestyle="-", color='black')
        fig.set_tight_layout(True)
        ax = plt.gca()
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.1)
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        # Transform the figure as a widget and add this widget to the screen
        widget = FigureCanvasKivyAgg(fig)
        self.ids.LoadBathGraphID.add_widget(widget)

class CreateBathPopup(Popup):
    
    """ Popup dedicated to the set of parameters allowing to define the 
        cross-section type chosen by the user """
        
    def RectTextInput(self):
        # Rectangle cross-section case
        self.choice = 'rectangle'
        self.ids.GridLayoutBath.padding = ['40sp', '140sp','40sp', '0sp']
        self.ids.GridLayoutBath.spacing = '60sp'
        self.nameFile = TextInput(multiline=False,hint_text='name of the file', size_hint = (0.45,0.2), pos_hint = {'top': 1.65,'center_x':0.5})
        self.L = TextInput(multiline=False,hint_text='L value', size_hint = (0.12,0.2), pos_hint = {'top': 1.2,'center_x':0.5})
        self.H = TextInput(multiline=False,hint_text='H value', size_hint = (0.13,0.2), pos_hint = {'center_y':0.5, 'right':0.91})
        self.RefPoint = TextInput(multiline=False,hint_text='Coordinates', size_hint = (0.19,0.2))
        self.ids.RelLayout.add_widget(self.nameFile)
        self.ids.RelLayout.add_widget(self.L)
        self.ids.RelLayout.add_widget(self.H)
        self.ids.RelLayout.add_widget(self.RefPoint)
        
    def TrapTextInput(self):
        # Trapezoidal cross-section case
        self.choice = 'trapezoidal'
        self.ids.GridLayoutBath.padding = ['40sp', '100sp','40sp', '0sp']
        self.ids.GridLayoutBath.spacing = '100sp'
        self.nameFile = TextInput(multiline=False,hint_text='name of the file', size_hint = (0.45,0.2), pos_hint = {'top': 1.5,'center_x':0.5})
        self.L = TextInput(multiline=False,hint_text='L value', size_hint = (0.12,0.2), pos_hint = {'top': 1.2,'center_x':0.485})
        self.H = TextInput(multiline=False,hint_text='H value', size_hint = (0.13,0.2), pos_hint = {'center_y':0.5, 'right':0.91})
        self.B = TextInput(multiline=False,hint_text='B value', size_hint = (0.13,0.2), pos_hint = {'center_x':0.485, 'top':0})
        self.RefPoint = TextInput(multiline=False,hint_text='Coordinates', size_hint = (0.19,0.2), pos_hint = {'right':0.3})
        self.ids.RelLayout.add_widget(self.nameFile)
        self.ids.RelLayout.add_widget(self.L)
        self.ids.RelLayout.add_widget(self.H)
        self.ids.RelLayout.add_widget(self.B)
        self.ids.RelLayout.add_widget(self.RefPoint)
        
    def ParabTextInput(self):
        # Parabolic cross-section case
        self.choice = 'parabolic'
        self.ids.GridLayoutBath.padding = ['40sp', '100sp','40sp', '0sp']
        self.ids.GridLayoutBath.spacing = '100sp'
        self.nameFile = TextInput(multiline=False,hint_text='name of the file', size_hint = (0.45,0.2), pos_hint = {'top': 1.5,'center_x':0.5})
        self.L = TextInput(multiline=False,hint_text='L value', size_hint = (0.12,0.2), pos_hint = {'top': 1.2,'center_x':0.485})
        self.H = TextInput(multiline=False,hint_text='H value', size_hint = (0.13,0.2), pos_hint = {'center_y':0.5, 'right':0.91})
        self.RefPoint = TextInput(multiline=False,hint_text='Coordinates', size_hint = (0.19,0.2), pos_hint = {'top': 0, 'right':0.4})
        self.ids.RelLayout.add_widget(self.nameFile)
        self.ids.RelLayout.add_widget(self.L)
        self.ids.RelLayout.add_widget(self.H)
        self.ids.RelLayout.add_widget(self.RefPoint)
        
    def FreeShapeTextInput(self):
        # Free cross-section case
        self.choice = 'freeshape'
        self.ids.GridLayoutBath.padding = ['40sp', '150sp','40sp', '0sp']
        self.ids.GridLayoutBath.spacing = '60sp'
        self.nameFile = TextInput(multiline=False,hint_text='name of the file', size_hint = (0.5,0.2), pos_hint = {'top': 1.85,'center_x':0.5})
        self.X = TextInput(multiline=False,hint_text='X value', size_hint = (0.5,0.2), pos_hint = {'top': 1.6,'center_x':0.5})
        self.Y = TextInput(multiline=False,hint_text='Y value', size_hint = (0.5,0.2), pos_hint = {'top': 1.4,'center_x':0.5})
        self.ids.RelLayout.add_widget(self.nameFile)
        self.ids.RelLayout.add_widget(self.X)
        self.ids.RelLayout.add_widget(self.Y)
        
     
    def createBathFileChoosen(self):
        # Function to store the chosen bathymetry's parameters  
        if (self.choice == 'rectangle'):
            x = list(map(float,self.RefPoint.text.split(',')))
            L = float(self.L.text)
            H = float(self.H.text)
            # Coordinates of the rectanguar shape are simply the four points starting from top left to top right
            points_x =  np.array([x[0],x[0],x[0]+L,x[0]+L])
            points_y =  np.array([x[1]+H,x[1],x[1],x[1]+H])
            points = np.array([points_x, points_y])
            
        if (self.choice == 'trapezoidal'):
            x = list(map(float,self.RefPoint.text.split(',')))
            L = float(self.L.text)
            H = float(self.H.text)
            B = float(self.B.text)
            # Coordinates of the trapezoidal shape are simply the four points starting from top left to top right
            points_x =  np.array([x[0]-(L-B)/2.0,x[0],x[0]+(L-B)/2.0,x[0]+B+(L-B)/2.0])
            points_y =  np.array([x[1]+H,x[1],x[1],x[1]+H])
            points = np.array([points_x, points_y]) 
            
        if (self.choice == 'parabolic'):
            x = list(map(float,self.RefPoint.text.split(',')))
            L = float(self.L.text)
            H = float(self.H.text)
            # Computation of the parabola coefficients using given parameters
            coeff = calc_parabola_vertex(x[0] - L/2.0, H, x[0], x[1],x[0] + L/2.0, H)
            # Computation of the coordinates of 100 points on the parabola defined by the parameters given
            # The number 100 is arbitrary and can be changed
            points_x = np.linspace(x[0] - L/2.0, x[0] + L/2.0, num=100)
            y = []
            for elt in points_x:
                y.append(coeff[0]*(elt**2) + coeff[1]*elt + coeff[2])
            points_y =  np.array(y)
            points = np.array([points_x, points_y]) 
            
        if (self.choice == 'freeshape'):
            # Coordinates of all points given by the user
            points_x = list(map(float,self.X.text.split(',')))
            points_y = list(map(float,self.Y.text.split(',')))
            points = np.array([points_x, points_y]) 
            
        # we take the transpose of the points array to have the data in two columns
        points = points.T
        # Save the result in a txt file of the name given by the user in a folder section/files/...
        with open('sections/'+'files/'+self.nameFile.text+'.txt', 'w+') as f:
            np.savetxt(f, points, fmt=['%f','%f'], delimiter=',')
        
        # we must set the variable of the bathymetry bath file to the one created
        app = App.get_running_app()
        app.BATHFILEPATH = 'sections/'+'files/'+ self.nameFile.text + '.txt'


## RIVER VIDEO FLOW SCREEN

class LoadingVideo(Screen):
    
    """ Screen regarding the loading of the river video and others parameters """
    
    def showDuration(self,path):
        # Compute the duration of the selected video
        x = re.findall(".mov$|.MOV$|.mp4$|.MP4$|.avi$|.AVI$",path[0])
        if (x == []):
            return ('0')
        cap = cv2.VideoCapture(path[0])
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps
        return ('%.2f'%duration)
    
    def registerVideoRiverPath(self,path, startTime, endTime, step):
        # If the stabilization is not chosen this method is called when the parameters
        # are loaded
        app = App.get_running_app()
        app.VIDEOSTEP = step
        app.VIDEOFILEPATH = path[0]
        app.VIDEORANGE = [startTime, endTime]
        
    def stabilizationPart(self, path, startTime, endTime, step):
        # If the stabilization is chosen this method is called when the parameters
        # are loaded
        app = App.get_running_app()
        app.VIDEOSTEP = step
        pathFolder = os.path.dirname(path[0])
        base=os.path.basename(path[0])
        names = os.path.splitext(base)
        newName = names[0]+ 'stabVersion' +names[1]
        # Stabilization method from stablization.py file is launched
        stabilization(path[0],newName)
        # The video file path is the one of the stabilized video
        app.VIDEOFILEPATH = pathFolder+ '\\' + newName 
        app.VIDEORANGE = [startTime, endTime]


## CALIBRATION SCREENS

class LoadFileCalibPopup(Popup):
    
    """ Popup that allows the user to select the calibration file if 
        calibration has already been performed for the camera used """
        
    loadFile = ObjectProperty()
    
class ComputationCalibPopup(Popup):
    
    """ Popup that asks the different parameters required for the calibration
        to the user """
    # the function computeCalib of the Calibration class (see after) is put
    # has an objectProperty to be able to use it in the popup 
    computeCalib = ObjectProperty()
    
class LoadingParamCalibPopup(Popup):
    
    """Popup that asks the different camera parameters to symply write them in a file"""
    
    loadParam = ObjectProperty()

class Calibration(Screen):
        
    """ Screen that proposes to load or compute calibration results """

    def loadFile(self, filenameExisting):
        # In this case just store calibration file path and perform
        # calibration on the river video frames
        app = App.get_running_app()
        app.CALIBRATIONFILE = filenameExisting[0]
        # Undistort video frames using function of Calibration.py file
        app.VIDEOFILEPATH = applyCalibrationOnVideoFrames(app.VIDEOFILEPATH, app.VIDEORANGE, app.CALIBRATIONFILE)
        app.CALIB = True
        
    def computeCalib(self, filename, videoFileName, boardDim, sizeSquare, nbrImageExtract):
        # In this case perform the calibration and store the result and undistort river video frames
        app = App.get_running_app()
        # Retrieve the board dimension, size of square and nb of images extract
        boardDim = list(map(int, boardDim.split(',')))
        sizeSquare = float(sizeSquare)
        nbrImageExtract = int(nbrImageExtract)
        # Call the function written in the calibration.py file which will save the calibration parameters in a .npy file 
        calibrationCamera(filename, videoFileName[0], boardDim, sizeSquare, nbrImageExtract)
        app.CALIBRATIONFILE = filename+'.npy'
        # Undistort video frames
        app.VIDEOFILEPATH = applyCalibrationOnVideoFrames(app.VIDEOFILEPATH, app.VIDEORANGE, app.CALIBRATIONFILE)
        app.CALIB = True
        
    def loadParam(self, filename, distCoeffs, cx, cy, fovx, fovy, fovdiag):
        app = App.get_running_app()
        distCoeffs = np.asarray(list(map(int, distCoeffs.split(','))))
        knownCalibrationParam(filename, distCoeffs, cx, cy, fovx, fovy, fovdiag)
        app.CALIBRATIONFILE = filename+ '.npy'
        app.VIDEOFILEPATH = applyCalibrationOnVideoFrames(app.VIDEOFILEPATH, app.VIDEORANGE, app.CALIBRATIONFILE)
        app.CALIB = True
        

## ORTHORECIFICATION SCREENS

class LoadingDistOrthoPopup(Popup):
    
    """ Popup that asks real distances between markers/Ground Control Points 
        in meters """
        
    # SetRealDistancesfunction of the next class put has objectproperty to
    # access it in the popup
    SetRealDistances = ObjectProperty()
    
class DistancesNotFound(Popup):
    
    """ Popup that notifies the user that he tries to load whitout writing any distances """
    
    pass

class OrthoParamNotFound(Popup):
    
    """ Popup that notifies the user that he did not select correctly all 
        the parameters for the orthorectification"""
    
    pass


class OrthoRectification(Screen):   
    
    """ Screen that performs the orthorectification """
    
    def on_enter(self):
        self.ids.OrthoGraphID.clear_widgets()
        # The choicePtsSrc and choiceMask are there to differentiate click events
        # for markers points or for masks in the onclick function depending on
        # what the user wants to give
        self.choicePtsSrc = False
        self.choiceMask = False
        self.pts_src = []
        self.pts_mask = []
        app = App.get_running_app()
        
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        vid.release()
        # Image on which the user will choose the different points is the first
        # frame of the video
        self.img = frame
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(frame)
        # Tow variables that allows to draw directly the points/lines when the 
        # user chooses points on the figure
        # by changing their values
        self.line1, = self.ax.plot(self.pts_src[::2],self.pts_src[1::2], 'r.',markersize=15)
        self.line2, = self.ax.plot(self.pts_mask[::2],self.pts_mask[1::2], 'r-',linewidth=2)
        # Add the figure widget to the screen
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.OrthoGraphID.add_widget(widget)
        # Link the click mouse event to the function onclick of the class
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        
    def SetRealDistances(self,dst):
        # function to put the information of the popup accessible inside the class 
        self.real_dst = dst
        # Set app.ORTHO to true since the user performed ortho
        app = App.get_running_app()
        app.ORTHO = True
        
        
    def onclick(self,event):
        # function that manage the clicks inputs according to the choice of the user
        if (self.choicePtsSrc and len(self.pts_src) < 8):
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            # update points
            self.pts_src += [x, y]
            # update graphs
            self.line1.set_xdata(self.pts_src[::2])
            self.line1.set_ydata(self.pts_src[1::2])
            self.fig.canvas.draw()
            
        elif self.choiceMask:
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            # update points
            if event.button == 3:
                # if the click is a right one close the mask by adding the first point 
                self.pts_mask += self.pts_mask[:2]                
            else:
                self.pts_mask  += [x, y]
            # update graphs
            self.line2.set_xdata(self.pts_mask[::2])
            self.line2.set_ydata(self.pts_mask[1::2])
            self.fig.canvas.draw()    
        
    def selectSrcPoints(self):
        # Erase previous data and set boolean values for the source points selection
        self.choicePtsSrc = True
        self.choiceMask = False
        self.pts_src = []
        self.line1.set_xdata(np.array([]))
        self.line1.set_ydata(np.array([]))
        self.fig.canvas.draw()
        
    def selectMask(self):
        # Erase previous data and set boolean values for the mask selection
        self.choicePtsSrc = False
        self.choiceMask = True
        self.pts_mask = []
        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        self.fig.canvas.draw()

    def registerInformation(self):
        #register information and draw shape registered 
        if self.choicePtsSrc:
            if(self.pts_src == []):
                print('No points selected')
            else:
                self.src = np.array(list(zip(self.pts_src[::2],self.pts_src[1::2])))
                #self.src = np.array([[373.676346, 468.333626],[1590.97224, 406.20081], [1743.134237, 648.39197], [175.86576, 635.711813]])
                
                #print(self.src)
                plt.plot(self.pts_src[::2],self.pts_src[1::2],'b.', markersize=15)
                # update the graph
                self.fig.canvas.draw()

            
        if self.choiceMask:
            if (self.pts_mask == []):
                print('No mask selected')
            else:
                self.mask = np.array(list(zip(self.pts_mask[::2],self.pts_mask[1::2])), dtype = np.int32)
                #print(self.mask)
                #self.mask =  np.array([[1178, 678],[115, 645],[353, 422],[1629, 369],[1796, 683]], dtype = np.int32)
                
                plt.plot(self.pts_mask[::2],self.pts_mask[1::2],'b-', linewidth=2)
                # update the graph
                self.fig.canvas.draw()
    
    def LoadPts(self):
        # Store orthorectification parameters in the application
        app = App.get_running_app()
        if(self.pts_src == []): #if the user did not select any points and try to load
            app.ORTHOPARAMS['pts_src'] = []
        elif(self.pts_mask == []):#if the user did not select any mask and try to load
            app.ORTHOPARAMS['pts_mask'] = []
        else:
            app.ORTHOPARAMS['pts_src'] = self.src
            app.ORTHOPARAMS['pts_mask'] = self.mask
            app.ORTHOPARAMS['img'] = self.img
            app.ORTHOPARAMS['L'] = self.real_dst
        

            self.pts_src[0] = self.src[0][0]
            self.pts_src[1] = self.src[0][1]
            self.pts_src[2] = self.src[1][0]
            self.pts_src[3] = self.src[1][1]
            self.pts_src[4] = self.src[2][0]
            self.pts_src[5] = self.src[2][1]
            self.pts_src[6] = self.src[3][0]
            self.pts_src[7] = self.src[3][1]

        
            dist1_pixel = np.sqrt((self.pts_src[::2][1] - self.pts_src[::2][0])**2 + \
                  (self.pts_src[1::2][1] - self.pts_src[1::2][0])**2)
            dist1_real = self.real_dst[0] 
            self.scaling_factor1 = dist1_pixel/dist1_real
        
            dist2_pixel = np.sqrt((self.pts_src[::2][2] - self.pts_src[::2][1])**2 + \
                  (self.pts_src[1::2][2] - self.pts_src[1::2][1])**2)
            dist2_real = self.real_dst[1] 
            self.scaling_factor2 = dist2_pixel/dist2_real
        
            dist3_pixel = np.sqrt((self.pts_src[::2][3] - self.pts_src[::2][2])**2 + \
                  (self.pts_src[1::2][3] - self.pts_src[1::2][2])**2)
            dist3_real = self.real_dst[2] 
            self.scaling_factor3 = dist3_pixel/dist3_real
        
            dist4_pixel = np.sqrt((self.pts_src[::2][0] - self.pts_src[::2][3])**2 + \
                  (self.pts_src[1::2][0] - self.pts_src[1::2][3])**2)
            dist4_real = self.real_dst[3] 
            self.scaling_factor4 = dist4_pixel/dist4_real
            
            dist5_pixel = np.sqrt((self.pts_src[::2][0] - self.pts_src[::2][2])**2 + \
                  (self.pts_src[1::2][0] - self.pts_src[1::2][2])**2)
            dist5_real = self.real_dst[4] 
            self.scaling_factor5 = dist5_pixel/dist5_real
            
            dist6_pixel = np.sqrt((self.pts_src[::2][1] - self.pts_src[::2][3])**2 + \
                  (self.pts_src[1::2][1] - self.pts_src[1::2][3])**2)
            dist6_real = self.real_dst[5] 
            self.scaling_factor6 = dist6_pixel/dist6_real            
      
            self.scaling_factor = (self.scaling_factor1 + self.scaling_factor2 + self.scaling_factor3 \
                                   + self.scaling_factor4 + self.scaling_factor5 + self.scaling_factor6)/6
            
            #self.scaling_factor = 100
            
            pts_src, pts_mask, img, L = app.ORTHOPARAMS['pts_src'], app.ORTHOPARAMS['pts_mask'], app.ORTHOPARAMS['img'], app.ORTHOPARAMS['L']
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # use of the orthorectificationComputation function from the homography.py file to compute the homography matrix h
            img_masked, img_rectified, self.h, \
                self.Xmin, self.Ymin = orthorectificationComputation(img,
                                                                     self.real_dst, 
                                                                     self.src,
                                                                     self.mask,
                                                                     self.scaling_factor)
            app.ORTHOPARAMS['img_rectified'] = img_rectified
            app.ORTHOPARAMS['h'] = self.h
            app.ORTHOPARAMS['Xmin'] = self.Xmin
            app.ORTHOPARAMS['Ymin'] = self.Ymin
            app.ORTHOPARAMS['scaling_factor'] = self.scaling_factor
            #print(self.scaling_factor)

## WATER LEVEL SCREENS


class WaterLevel(Screen):
    
    """ Screen that offers the different choices for the computation 
        of the water level"""
    pass

class LevelPopup(Popup):
    
    """ Water level popup where the user gives the water level value """
    
    def registerLevel(self):
        app = App.get_running_app()
        # the given value should be the elevation of the water level
        # given in the same reference as the bathymetry curve
        app.WATERLEVEL = float(self.ids.levelID.text)
        
class LengthPopup(Popup):
    
    """ Water level popup where the user gives the river length value """
    
    def registerLevel(self):
        app = App.get_running_app()
        filename = app.BATHFILEPATH
        L = float(self.ids.lengthID.text)
        wl, xc, ycs = findWaterLevel(filename,L)
        app.WATERLEVEL = round(wl[0],3)
        #print(app.WATERLEVEL)
        
class WaterLevelNotFound(Popup):
    
    """Popup that notifies the user that he did not write any value for the water level """
    
    pass
        
class ComputeLevelPopup(Popup):
    
    """ Water level popup concerning the alternative methods: 
        Angle and Height method and Image method. Once the river 
        section length in meter is known this popup compute the water 
        level and display the results """
    
    def setGraphIntersection(self,xcs,ycs):
        # Function that displays the bathymetry curve and the line at
        # the water level height. xcs and ycs are the points coorinates of the 
        # line at water level
        self.ids.intersectionGraphID.clear_widgets() # clear graphs
        app = App.get_running_app()
        # Load bathymetry data
        dem = np.loadtxt(app.BATHFILEPATH , delimiter = ',')
        x = np.array(dem[:,0])
        y1 = np.array(dem[:,1])
        fig = plt.figure()
        plt.plot(x,y1)
        plt.plot(xcs,ycs)
        for xc, yc in zip(xcs, ycs):
            plt.plot(xc, yc, 'ko', ms=5)
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.rc('grid', linestyle="-", color='black')
        fig.set_tight_layout(True)
        ax = plt.gca()
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.1)
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        # Add figure widget to the screen
        widget = FigureCanvasKivyAgg(fig)
        self.ids.intersectionGraphID.add_widget(widget)

class LengthNotFound(Popup):
    
    """Popup that is displayed when the length selected in the image method is not found in the section"""
    
    pass
    
class DEMPopup(Popup):
    
    """ Water level popup concerning the Hellebaut adapted method using DEM """
    
    def showBathPlot(self,f):
        #Function that store the information gathered in the popup
        precision = float(self.ids.PrecisionID.text)*1e-3# precision given in mm/pixel but in the following it must be in meter
        distx = float(self.ids.DistanceID.text)
        domaine = self.ids.DomainID.text.split('\n')
        dom_x = list(map(float,domaine[0].split(',')))
        dom_y = list(map(float,domaine[1].split(',')))
        bathDem = skiTif.imread(f[0])
        app = App.get_running_app()
        data = np.loadtxt(app.BATHFILEPATH, delimiter = ',')
        X = data[:,0]
        width = X[-1]
        ind = np.arange(1,round(distx*1/precision)+1)
        Xdem = np.linspace(0.0,width-precision,int(round((width-precision)/precision)+1))
        Xdem = [Xdem[i] for i in ind]
        Y0 = int(bathDem.shape[0] - abs(dom_y[0])*1000)
        X0 = int(abs(dom_x[0])*1000);
        Ydem = bathDem[Y0,ind+X0]
        pointsDEM = np.array([Xdem, Ydem])
        pointsDEM = pointsDEM.T
        with open('DEM/currentDEM.txt', 'w') as f:
            np.savetxt(f, pointsDEM, fmt=['%f','%f'], delimiter=',')
        app.WATERLEVELPATH = 'DEM/currentDEM.txt'
        
class WaterLevelDEM(Screen):
    
    """ Water level screen for Hellebaut adapted method using DEM """
    
    def on_enter(self):
        self.ids.DEMGraphID.clear_widgets()
        app = App.get_running_app()
        dem = np.loadtxt(app.WATERLEVELPATH , delimiter = ',')
        self.Xdem = dem[:,0]
        Ydem = dem[:,1]
        data = np.loadtxt(app.BATHFILEPATH, delimiter = ',')
        X = data[:,0]
        Y = data[:,1]
        self.Yinterest = np.interp(self.Xdem, X, Y)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        plt.plot(self.Xdem,self.Yinterest,label= 'Reference bathymetry')
        plt.plot(self.Xdem,Ydem,label= 'DEM bathymetry')
        leg = self.ax.legend(facecolor='black')
        leg_texts = leg.get_texts() 
        leg_texts[0].set_color('w') 
        leg_texts[1].set_color('w') 
        # Compute the difference curve 
        diff = abs(self.Yinterest - Ydem)
        ind = argrelextrema(diff, np.less)[0]
        indPoint = 0
        # Compute the mean of the minima
        moyenne = np.mean(diff[ind])
        # Loop where the first minima below the average value is returned
        # The X cooridnates must starts from the riverbank to the center 
        # of the river
        for i in ind[::-1]:
            if diff[i] < moyenne :
                indPoint = i
                break
        self.Xpoint = self.Xdem[indPoint]
        self.Ypoint = Ydem[indPoint]
        self.line1, = self.ax.plot(self.Xpoint,self.Ypoint, 'w.',markersize=15)
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.rc('grid', linestyle="-", color='black')
        self.fig.set_tight_layout(True)
        ax = plt.gca()
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.1)
        ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.DEMGraphID.add_widget(widget)
        
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
        
        self.ids.labelWatLevID.text = 'Water Level : '+ '%4.3f' % self.Ypoint
        app = App.get_running_app()
        app.WATERLEVEL = self.Ypoint
        
    def onclick(self,event):
        # function to allow the user to click on the graph where the divergence between the two curves occurs
        # transfrom pixel coordinates into coordinates relative to the axes of the plot
        x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
        ind = self.find_nearest(self.Xdem,x)
        self.line1.set_xdata(self.Xdem[ind])
        self.line1.set_ydata(self.Yinterest[ind])
        self.ids.labelWatLevID.text = 'Water Level : '+ '%4.3f' % self.Yinterest[ind]
        app = App.get_running_app()
        app.WATERLEVEL = self.Yinterest[ind]
        self.fig.canvas.draw()
        # next we will need to look at which point is the closet to the click one
        
    def find_nearest(self,array, value):
        # return closet point to the click of the user on the reference curve
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx
    

class WaterLevelOrtho(Screen):  
    
    """ Water level computation using orthorectified result """
    
    def RiverLength(self):
        app = App.get_running_app()
        L = app.ORTHOPARAMS['LengthRiver']
        # call the function findWaterLevel from the findIntersection.py file
        # wl is the water level, xcs and ycs are the intersection points 
        # coordinates on the bathymetry curve
        wl,xcs,ycs = findWaterLevel(app.BATHFILEPATH,L)
        app.WATERLEVEL = wl[0]
        return (L,wl,xcs,ycs)
    
    def on_enter(self):
        
        self.ids.RectifiefGraphID.clear_widgets()
        app = App.get_running_app()
        
        img_rectified = app.ORTHOPARAMS['img_rectified']
        self.h = app.ORTHOPARAMS['h'] # h is the homography matrix
        self.scaling_factor = app.ORTHOPARAMS['scaling_factor']
        self.img = img_rectified
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(img_rectified,cmap='gray')
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.RectifiefGraphID.add_widget(widget)
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
    
        self.pts_section = []
        self.line2, = self.ax.plot(self.pts_section[::2],self.pts_section[1::2], 'r.',markersize=15)
        self.choiceSectPts = False
        
    def onclick(self,event):
        # selection of the section point of the river (if they are not aligned
        # the image will be rotate to make them aligned) The goal is to easily 
        # retrieve perpendicular velocity vectors after
        if self.choiceSectPts:
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            self.pts_section  += [x, y]
            self.line2.set_xdata(self.pts_section[::2])
            self.line2.set_ydata(self.pts_section[1::2])
            self.fig.canvas.draw()    
        
    def selectSectPoints(self):
        self.choiceSectPts = True
        self.pts_section = []
        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        self.fig.canvas.draw()
       
    def saveInformation(self):

        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        plt.plot(self.pts_section[::2],self.pts_section[1::2],'b.', markersize=15)
        self.fig.canvas.draw()
        self.pts_section = np.array(list(zip(self.pts_section[::2],self.pts_section[1::2])))
        # The image is rotated to make the 2 section points aligned
        self.img_rotated, self.angle_rotation = rotation(self.img, self.pts_section)
        
        app = App.get_running_app()
        
        # compute section at water level length in meter. To get in meter
        # the value must be divided by the scaling factor used to scale the orthorectified image
        L = (1/self.scaling_factor)*np.sqrt((self.pts_section[1,0] - self.pts_section[0,0])**2 + \
                (self.pts_section[1,1] - self.pts_section[0,1])**2)
        
        print('Largeur d eau calculée : ' , L)

        app.ORTHOPARAMS['LengthRiver'] = L
    
class OrthoNotSelected(Popup):
    
    """Popup to tells the user that he must do an orthorectification to 
        use Image Method"""
    
    pass


class WaterLevelComputation(Screen):
    
    """ In the Angle and Height method computation of the water level """
    
    def RiverLength(self,closeImage,farImage,deltaH):
        app = App.get_running_app()
        L,H = droneGeometryWaterLevel(app.CALIBRATIONFILE, closeImage[0], farImage[0], deltaH)
        # use of the findWaterLevel from the findIntersection.py file
        wl,xcs,ycs = findWaterLevel(app.BATHFILEPATH,L)
        app.WATERLEVEL = wl[0]
        return (L,wl,xcs,ycs)
    
class CalibNotSelected(Popup):
    
    """ Popup to tell the user that he must do a calibration to 
        perform Angle and Heigth Method"""
        
    pass

class LengthNotFoundCalib(Popup):
    
    """ Popup that prevent the user that the length chosen by Angle and Height method
        is not found in the section"""
    
    pass

## REGION OF INTEREST AND MASKS SCREENS

class ROIMASK(Screen):
    
    """ Screen which defines the Region of Interest and the masks """

    def on_enter(self):
        # the self.choiceROI and self.choiceMask variables allows to activate the 
        # ROI selection or the masks one
        self.choiceROI = False
        self.choiceMask = False
        self.ROI = []
        self.pts_ROI = []
        self.pts_Mask = []
        self.Mask = []
        
        app = App.get_running_app()
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        ret, frame = vid.read()
        self.img = frame
            
        
        self.ids.ROIselection.clear_widgets()
        self.fig = plt.figure()        
        self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(self.img)
        self.ax = plt.gca()
        self.ax.set_facecolor('#33333d')
        self.line1, = self.ax.plot(self.pts_ROI[::2],self.pts_ROI[1::2], 'g-',linewidth=1.5)
        self.line2, = self.ax.plot(self.pts_Mask[::2],self.pts_Mask[1::2], 'r-',linewidth=1.5)
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        
        widget = FigureCanvasKivyAgg(self.fig)
        
        self.ids.ROIselection.add_widget(widget)
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
    

    def on_motion(self,event):
        # function to draw rectangle of ROI selection as the user moves 
        # the mouse on the screen
        if (self.choiceROI == True and len(self.pts_ROI) > 1):
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            self.line2.set_xdata([self.pts_ROI[0], x, x, self.pts_ROI[0], self.pts_ROI[0]])
            self.line2.set_ydata([self.pts_ROI[1], self.pts_ROI[1], y, y, self.pts_ROI[1]])
            self.fig.canvas.draw()

    def selectROI(self):
        # just reinitialize the masks and roi variables and activate the choiceROI
        self.choiceROI = True
        self.choiceMask = False
        self.ROI = []
        
        self.line1.set_xdata(np.array([]))
        self.line1.set_ydata(np.array([]))
        self.fig.canvas.draw()

    def selectMask(self):
        # just reinitialize the masks and roi variables and activate the choiceMask
        self.choiceROI = False
        self.choiceMask = True
        self.pts_Mask = []
        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        self.fig.canvas.draw()

        
    def onclick(self,event):
        
        if self.choiceROI:
            if len(self.pts_ROI) == 0:
                self.motionConnect = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
            if len(self.pts_ROI) == 2:
                self.ax.figure.canvas.mpl_disconnect(self.motionConnect)
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            self.pts_ROI += [x,y]
            self.fig.canvas.draw()
            

        elif self.choiceMask:
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            if event.button == 3:
                self.pts_Mask += self.pts_Mask[:2]                
            else:
                self.pts_Mask  += [x, y]
            self.line2.set_xdata(self.pts_Mask[::2])
            self.line2.set_ydata(self.pts_Mask[1::2])
            self.fig.canvas.draw()     
            
    def onselect(self, eclick, erelease):
        pass
            
    def registerInformation(self):
        # register the new mask or ROI added and draw shape registered
        if self.choiceROI:
            if (self.pts_ROI == []):#the user can now register and load without select ROI and the program doesn't close anymore
                print('No region of interest selected')
            else:
                self.ROI += self.pts_ROI
                x = [self.pts_ROI[0],self.pts_ROI[2],self.pts_ROI[2],self.pts_ROI[0],self.pts_ROI[0]]
                y = [self.pts_ROI[1],self.pts_ROI[1],self.pts_ROI[3],self.pts_ROI[3],self.pts_ROI[1]]
                plt.plot(x,y,'g-',linewidth=1.5)
                self.ax.fill(x,y,'g',alpha=0.3)
                self.fig.canvas.draw()
                
        if self.choiceMask:
            if(self.pts_Mask != []):
                self.Mask += [self.pts_Mask]
                self.ax.fill(self.Mask[-1][::2], self.Mask[-1][1::2],'r',alpha=0.3)
                plt.plot(self.Mask[-1][::2], self.Mask[-1][1::2],'r-',linewidth=1.5)
                self.fig.canvas.draw()
            else:
                print('No mask selected')
            
    def loadTheResults(self):
        # save the different masks and the ROI as global variables in the app
        # since the masks where just points so far this function turns them
        # into real masks boolean arrays
        app = App.get_running_app()
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        ret, frame = vid.read()
        H,W = frame.shape[:2]
        vid.release()
        nbrOfMask = len(self.Mask)
        coordonnees = []
        img_mask = np.ones((H,W)).astype(bool)
        
        for i in range(nbrOfMask):
            coord = np.array(self.Mask[i])
            coord = coord.astype(int) # Pixel coordinates must be int
            coordonnees = np.array(list(zip(coord[::2], coord[1::2])))
            mask = np.ones((H,W))
            cv2.fillPoly(mask, [coordonnees], 0)
            img_mask = mask.astype(bool)*img_mask
        
        img_mask = ~img_mask
        
        if (len(self.ROI)>0):
            ROI = [int(self.ROI[1]),int(self.ROI[3]),int(self.ROI[0]),int(self.ROI[2])]
            app.ROI = np.array(ROI) 
            # only take the part of the mask that is inside the ROI
            img_mask = img_mask[ROI[0]:ROI[1],ROI[2]:ROI[3]]
            
        app.IMGMASKS = img_mask
        
        #print(app.ROI) # [ 406 742 71 1791]
        
        testMask = {}
        
        testMask = {'mask':app.IMGMASKS}
        
        
        np.save('testMask.npy',testMask)
        
        maskLoadTest = np.load('testMask.npy', allow_pickle = 'TRUE').item()
        
        
        Mask = maskLoadTest['mask']
        
        app.IMGMASKS = Mask
        #app.ROI = [ 207,  787,   87, 1857]
        


## FILTERS POPUPS AND SCREENS
        
# The following classes of popup are the different popup of the filters implemented
# in the application the different object property are the functions inside the screen class
# that need to be acessible from the popups 
      
class CLAHEPopup(Popup):
    selectFilter = ObjectProperty()

class CLAHEInformation(Popup):    
    pass

class IntensityCappingPopup(Popup):
    selectFilter = ObjectProperty()
    findParamIntCapping = ObjectProperty()
    
class IntensityCappingInformation(Popup):    
    pass
    
class IntensityHighPassPopup(Popup):
    selectFilter = ObjectProperty()
    findParamHighPass = ObjectProperty()
    
class IntensityHighPassInformation(Popup):    
    pass
    
class MeanDenoisingPopup(Popup):
    selectFilter = ObjectProperty()
    
class MeanDenoisingInformation(Popup):    
    pass
    
class ContrastBrightnessPopup(Popup):
    selectFilter = ObjectProperty()
    
class ContrastBrightnessInformation(Popup):    
    pass
    
class GammaCorrectionPopup(Popup):
    selectFilter = ObjectProperty()
    
class GammaCorrectionInformation(Popup):    
    pass
    
class CLAHEInformation(Popup):    
    pass

class Filters(Screen):     
    
    """" Screen that proposes the differents filters to apply on the
        image which is the output of the previous step of ROI and masks selection """
    
    def on_enter(self):
        self.filtersChosen = []
        self.parametersFilterChosen = []
        
        app = App.get_running_app()
        
        
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        framecount=0
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        while(True):
            # Capture frame at the range[0] to see the particules
            ret, image = vid.read()
            if(app.VIDEORANGE[0]==0) or app.CALIB==True:
                frame=image
                break
            else:   
                framecount += 1
                if (framecount == (fps*app.VIDEORANGE[0])):
                    frame=image
                    break
        
        self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        app.IMG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if len(app.ROI) == 4:
            self.img =  self.img[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
        vid.release()
        self.img = np.ma.masked_array(self.img, app.IMGMASKS)
        self.newImg = self.img.copy()
        
        self.imagesFilters = [self.img]
        # clear the previous clear useful when the user come back to the previous screen
        self.ids.filterGraphID.clear_widgets()
        
        fig = plt.figure()
       
        plt.imshow(self.img, cmap='gray', vmin=0, vmax=255)
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        widget = FigureCanvasKivyAgg(fig)
        self.ids.filterGraphID.add_widget(widget)
                              
    def findParamIntCapping(self):
        # method to find the clip value for the IntensityCapping filter
        img_flatten = self.img.flatten()
        md = np.median(img_flatten)
        std = np.std(img_flatten)
        threshold = md+2*std
        return threshold
        
    def findParamHighPass(self):
        # method that determine the factor in the HighPass filter based 
        # on the image
        img_flatten = self.img.flatten()
        maximum = max(img_flatten)
        return 255/maximum

    def selectFilter(self, choice, *args):
        self.ids.filterGraphID.clear_widgets()
        fig = plt.figure() 
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        # Once a filter is selection the image display will be the previous image
        # at which the filter has been applied
        self.newImg = filtersImage(self.img, choice, *args)
        app = App.get_running_app()
        self.newImg = np.ma.masked_array(self.newImg, app.IMGMASKS)
        
        self.currentParam = args
        
        plt.imshow(self.newImg, cmap='gray', vmin=0, vmax=255)
        widget = FigureCanvasKivyAgg(fig)
        self.ids.filterGraphID.add_widget(widget)
    
    def registerFilter(self, nameFilter):
        self.parametersFilterChosen.append(self.currentParam)
        self.filtersChosen.append(nameFilter)
        self.imagesFilters.append(self.newImg)
        self.img = self.newImg.copy()
        
    def removeFilter(self):
        # this function removes the last filter added
        if (self.filtersChosen == []):
            print('No filter selected')
        else :
            self.parametersFilterChosen = self.parametersFilterChosen[:-1]
            self.filtersChosen = self.filtersChosen[:-1]
            self.imagesFilters = self.imagesFilters[:-1]
            self.img = self.imagesFilters[-1]
            self.ids.filterGraphID.clear_widgets()
            fig = plt.figure() 
            ax = plt.gca()
            ax.set_facecolor('#33333d')
            fig.patch.set_facecolor('#33333d')
            plt.axis('off')
            plt.imshow(self.img, cmap='gray', vmin=0, vmax=255)
            widget = FigureCanvasKivyAgg(fig)
            self.ids.filterGraphID.add_widget(widget)
            
    def plotHistogram(self, filepath):
        
        app = App.get_running_app()
        filepathHisto = applyFilterOnVideoFrames(filepath, app.VIDEORANGE, self.filtersChosen, self.parametersFilterChosen)
        vidcap = cv2.VideoCapture(filepathHisto)
        success,image = vidcap.read()
        count = 0
        while success and count==0:
            cv2.imwrite("frameForHisto.jpg", image)     # save frame as JPEG file      
            success,image = vidcap.read()
            count = 1
            
        #imagehisto = filtersImage(self.img, self.filtersChosen, self.parametersFilterChosen)
        #cv2.imwrite("frametest.jpg",imagehisto)
        
        self.ids.filterGraphID.clear_widgets()
        fig = plt.figure()
        img = cv2.imread('frameForHisto.jpg',0)
        hist,bins = np.histogram(img.flatten(),256,[0,256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(hist.max()) / cdf.max()
        plt.plot(cdf_normalized)
        plt.hist(img.flatten(),256,[0,256], color='orange')
        plt.rc('grid', linestyle="-", color='black')
        plt.xlim([0,256])
        plt.legend(('cdf','histogram'), loc = 'upper left')
        ax = plt.gca()
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.1)
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        #plt.show()
        widget = FigureCanvasKivyAgg(fig)
        self.ids.filterGraphID.add_widget(widget)
           
    def saveFilterChosen(self):
        # save all the filters chosen and apply them on the frames
        app = App.get_running_app()
        app.FILTERS = self.filtersChosen
        app.FILTERSPARAM = self.parametersFilterChosen
        if len(app.FILTERS) != 0:
            # if filters chosen then apply them on the video frames using 
            # the applyFilterOnVideoFrames function of the filtersImage.py file
            app.VIDEOFILEPATH = applyFilterOnVideoFrames(app.VIDEOFILEPATH, app.VIDEORANGE, app.FILTERS, app.FILTERSPARAM)
  
            
class FilterNotFound(Popup):
    
    """ Popup that notifies the user he did not select any filter"""
    pass
    
class FilterApplied(Popup):
    
    """ Popup that notifies the user that the filter selected was correctly applied"""
    
    pass
        
## PIV ANALYSIS SCREENS

class PIVAnalysis(Screen):
    
    """Screen that proposes the choice between single pass and multi-pass 
       PIV analysis"""
    
    pass

class PIVPopup(Popup):
    # Thread which manages the loading bar showing the advancement of the velocity
    # analysis
    launchThread = ObjectProperty()
    
class LoadingPopup(Popup):
    
    """ Popup that display the loading bar """
    
    def __init__(self, obj, **kwargs):
        super(LoadingPopup, self).__init__(**kwargs)
    
class SurfaceVelocity(Screen):
    
    """ Screen where the PIV analysis is performed """
    
    def on_enter(self):
        self.p = PIVPopup(launchThread=self.launchThread)
        self.p.open()
        app = App.get_running_app()
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        ret, frame = vid.read()
        
        # If no filter where applied the image need to be convert in grayscale
        # otherwise it is already done
        if len(app.FILTERS) == 0:
            self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            self.img = frame
        
        if len(app.ROI) == 4:
            self.img =  self.img[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
        vid.release()
        fig = plt.figure()
        plt.imshow(self.img, cmap='gray', vmin=0, vmax=255)
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        widget = FigureCanvasKivyAgg(fig)
        self.ids.VelocityGraphID.add_widget(widget)
        
    def launchThread(self,winsize,overlap, SNR):
        # launch of the thread that contains the progress bar
        self.popup = LoadingPopup(self)
        self.popup.open()
        threading.Thread(target=partial(self.computeVelocity, winsize ,overlap, SNR)).start()
    
    def update_bar(self, value, *args):
        # function that updates the progress bar value based on the frame where 
        # the video is
        self.popup.ids.labelID.text = '%d' % (value*100) + ' %'
        self.popup.ids.progBarID.value = value
        
    def computeVelocity(self,winsize,overlap,SNR):
        
        app = App.get_running_app()
        step = int(app.VIDEOSTEP)
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        fps =  round(vid.get(cv2.CAP_PROP_FPS))
                
        nbFramOfInterest = (app.VIDEORANGE[1]-app.VIDEORANGE[0])*fps/step #ajout du /step car barre de chargement ne tenait pas compte du step

        i = 0
        frameVideo = {}
        dt = 1.0/(fps/step)  # sec 
        print('Infos: The video has ', fps, ' frames per second and you selected a step of ', step, ' so the delta t is ', dt)
        velocity_field = {}
        # Store in a dictionary all the frames in grayscale. Store in a dictionary
        # because it is easier to find the frames inside the range chosen by the user
        # and to applied the step also given by the user
        while(vid.isOpened()):
            ret, frame = vid.read()
            if ret is True :
                frameVideo[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                i+=1
            else:
                break
        # ind_start and ind_end give the first frame and last one to analyse
        # from the range given by the user
        if app.CALIB ==True or app.FILTERS != []: 
            #if calib of filters applied, new video created and duration of vidéo had changed
            ind_start = 0
            ind_end = min(int(app.VIDEORANGE[1]*fps )-int(app.VIDEORANGE[0]*fps) -step ,len(frameVideo) -1 -step)
        else : 
            ind_start = int(app.VIDEORANGE[0]*fps)
            ind_end = min(int(app.VIDEORANGE[1]*fps -step) , len(frameVideo) -1-step)
            
        #vectors to write in the .txt file    
        vectu, vectv = np.array([]), np.array([])
        
        #count = 0
        
        for i,j in enumerate(range(ind_start,ind_end,step)):
            frame1 = frameVideo[j]
            frame2 = frameVideo[j+ step] # The second frame is the one which is a step frames form the first one
            
            
            # On these frames only the parts inside the ROI and without the masks 
            # regions are interesting 
            if len(app.ROI) == 4:
                frame1 =  frame1[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
                frame2 = frame2[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]

            mask = np.array(~app.IMGMASKS, dtype= np.int32)*255
            mask = mask.astype(np.uint8)         #mask vérifier: OK!
            
            frame1 = cv2.bitwise_and(frame1, mask) #mask vérifier: OK!
            frame2 = cv2.bitwise_and(frame2, mask) #mask vérifier: OK!
            
            
            # Using the OpenPIV function to perform the PIV analysis
            u0, v0, sig2noise = pyprocess.extended_search_area_piv( frame1.astype(np.int32),
                                                                     frame2.astype(np.int32),
                                                                     window_size=winsize,
                                                                     overlap=overlap,
                                                                     dt=dt,
                                                                     search_area_size=winsize,
                                                                     correlation_method='circular',
                                                                     subpixel_method='gaussian',
                                                                     sig2noise_method='peak2peak')
        
                                                                                        
            # coordinates of the interrogation window nodes where the velocity 
            # is computed
            x, y = pyprocess.get_coordinates( image_size = frame1.shape,
                                             search_area_size=winsize,
                                             overlap=overlap )

            ##############Differents method of validation####################
            
            #using correlation matrix
            u1 , v1, mask = validation.sig2noise_val( u0,
                                                      v0,
                                                      sig2noise,
                                                      threshold=SNR )
            
            #using comparision to a median value   
            #u1 , v1, mask = validation.local_median_val( u0, v0, 3, 3, size=1 )
            
            #using de standart deviation
            #u1 , v1, mask = validation.global_std( u0, v0, std_threshold = 3 )
            
            #check if the velocities are between two values
            #u1, v1, mask = validation.global_val(u0, v0, (-150,150), (-150,150))
            
            #validation using gloabl limits and std and local median
            #settings=windef.Settings()
            #u1, v1, mask = validation.typical_validation(u0, v0, sig2noise, settings)
            ##############################################################
            
            u2, v2 = filters.replace_outliers( u1,
                                               v1,
                                               method='localmean',
                                               max_iter=10,
                                               kernel_size=3 ) 
          
            
            velocity_field[i] = {'x':x,'y':y,'u':u2,'v':v2,'mask':mask}
        
            vectu = np.append(vectu, u2)
            vectv = np.append(vectv, v2)
            Clock.schedule_once(partial(self.update_bar,i/nbFramOfInterest))
            
            
        self.popup.dismiss()
        np.save('velocity.npy',velocity_field)
        
        #save velocity informations in a text file
        listotal = [vectu, vectv]
        f=open('Velocity.txt','w')
        f.write('u,v ')
        f.write("\n")
        np.savetxt(f, list(zip(*listotal)), delimiter=',')
        f.close()
        
        info = {}
        info['ROI'] = app.ROI
        info['mask'] = app.IMGMASKS
        

        np.save('maskandroi.npy',info)
        vid.release()
        # computation of the mean velocity field using the computeMeanVelocity function
        # of the meansVelocity.py file
        
        
        (x,y,u_mean,v_mean) = computeMeanVelocity(self.img)
        
        f=open('SP_u_mean.txt','w')
        f.write('single pass: u_mean ')
        f.write("\n")
        np.savetxt(f, u_mean, delimiter=';')
        f.close()
        
        f=open('SP_v_mean.txt','w')
        f.write('single pass: v_mean ')
        f.write("\n")
        np.savetxt(f, v_mean, delimiter=';')
        f.close()
        
        app.MEANVELOCITYDATA['x'] = x
        app.MEANVELOCITYDATA['y'] = y
        app.MEANVELOCITYDATA['u_mean'] = u_mean
        app.MEANVELOCITYDATA['v_mean'] = v_mean
        # display the mean velocity field
        self.ids.VelocityGraphID.clear_widgets()
        fig, ax = plt.subplots()
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(self.img, cmap='gray')
        plt.draw()
        ax.quiver(x, y, u_mean, v_mean, color='orange',width=0.001)    
        widget = FigureCanvasKivyAgg(fig)
        self.ids.VelocityGraphID.add_widget(widget)

class MultiPassPIVPopup(Popup):
    
    launchThread = ObjectProperty()

class SurfaceVelocityMultiPass(Screen):
    
    """ Screen where the multi-pass PIV analysis is performed """
    
    def on_enter(self):
        self.p = MultiPassPIVPopup(launchThread=self.launchThread)
        self.p.open()
        app = App.get_running_app()
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        ret, frame = vid.read()
        
        # If no filter where applied the image need to be convert in grayscale
        # otherwise it is already done
        if len(app.FILTERS) == 0:
            self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            self.img = frame
        
        if len(app.ROI) == 4:
            self.img =  self.img[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
        vid.release()
        fig = plt.figure()
        plt.imshow(self.img, cmap='gray', vmin=0, vmax=255)
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        widget = FigureCanvasKivyAgg(fig)
        self.ids.VelocityGraphID.add_widget(widget)
        
    def launchThread(self, winsizeFirstPass, winsize):
        # launch of the thread that contains the progress bar
        self.popup = LoadingPopup(self)
        self.popup.open()
        threading.Thread(target=partial(self.computeVelocity, winsizeFirstPass, winsize)).start()
    
    def update_bar(self, value, *args):
        # function that updates the progress bar value based on the frame where 
        # the video is
        self.popup.ids.labelID.text = '%d' % (value*100) + ' %'
        self.popup.ids.progBarID.value = value
        
    def computeVelocity(self,winsizeFirstPass,winsize):
        
        app = App.get_running_app()
        step = int(app.VIDEOSTEP)
        vid = cv2.VideoCapture(app.VIDEOFILEPATH)
        fps =  round(vid.get(cv2.CAP_PROP_FPS))
                
        nbFramOfInterest = (app.VIDEORANGE[1]-app.VIDEORANGE[0])*fps/step #ajout du /step car barre de chargement ne tenait pas compte du step

        i = 0
        frameVideo = {}
        dt = 1.0/(fps/step) # sec 
        print('Infos: The video has ', fps, ' frames per second and you selected a step of ', step, ' so the delta t is ', dt)
        velocity_field = {}
        # Store in a dictionary all the frames in grayscale. Store in a dictionary
        # because it is easier to find the frames inside the range chosen by the user
        # and to applied the step also given by the user
        while(vid.isOpened()):
            ret, frame = vid.read()
            if ret is True :
                frameVideo[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                i+=1
            else:
                break
        # ind_start and ind_end give the first frame and last one to analyse
        # from the range given by the user
        if app.CALIB ==True or app.FILTERS != []: 
            #if calib of filters applied, new video created and duration of vidéo had changed
            ind_start = 0
            ind_end = min(int(app.VIDEORANGE[1]*fps)-int(app.VIDEORANGE[0]*fps)-step,len(frameVideo) -1 - step)
        else : 
            ind_start = int(app.VIDEORANGE[0]*fps)
            ind_end = min(int(app.VIDEORANGE[1]*fps) - step, len(frameVideo) -1 - step)
            
        #vectors to write in the .txt file    
        vectu, vectv = np.array([]), np.array([])
        
        
        for i,j in enumerate(range(ind_start,ind_end,step)):
            frame1 = frameVideo[j]
            frame2 = frameVideo[j+ step] # The second frame is the one which is a step frames form the first one
            
            # On these frames only the parts inside the ROI and without the masks 
            # regions are interesting 
            if len(app.ROI) == 4:
                frame1 =  frame1[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
                frame2 = frame2[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]

            mask = np.array(~app.IMGMASKS, dtype= np.int32)*255
            mask = mask.astype(np.uint8)
            frame1 = cv2.bitwise_and(frame1, mask)
            frame2 = cv2.bitwise_and(frame2, mask)
            
            #multipass using windef (need the openpiv last version)    
            settings=windef.Settings()
            
            """First pass"""
            
            # Using the OpenPIV function to perform the PIV analysis
            u0, v0, sig2noise = pyprocess.extended_search_area_piv( frame1.astype(np.int32),
                                                                     frame2.astype(np.int32),
                                                                     window_size=64,
                                                                     overlap=32,
                                                                     dt=dt,
                                                                     search_area_size=64,
                                                                     correlation_method='circular',
                                                                     subpixel_method='gaussian',
                                                                     sig2noise_method='peak2peak')

                                                                                        
            # coordinates of the interrogation window nodes where the velocity 
            # is computed
            x, y = pyprocess.get_coordinates( image_size = frame1.shape,
                                             search_area_size=64,
                                             overlap=32 )

            ##############Differents method of validation####################
            
            #using correlation matrix
            u , v, mask = validation.sig2noise_val( u0,
                                                      v0,
                                                      sig2noise,
                                                      threshold=2 )
            
            #using comparision to a median value   
            #u1 , v1, mask = validation.local_median_val( u0, v0, 150, 150, size=1 )
            
            #using de standart deviation
            #u1 , v1, mask = validation.global_std( u0, v0, std_threshold = 3 )
            
            #check if the velocities are between two values
            #u1, v1, mask = validation.global_val(u0, v0, (-150,150), (-150,150))
            
            #validation using gloabl limits and std and local median
            #settings=windef.Settings()
            #u1, v1, mask = validation.typical_validation(u0, v0, sig2noise, settings)
            ##############################################################
            
            u_old, v_old = filters.replace_outliers( u,
                                               v,
                                               method='localmean',
                                               max_iter=10,
                                               kernel_size=3 ) 

            
            
           # u = np.ma.asarray(u_old,np.ma.nomask)
            #v = np.ma.asarray(v_old,np.ma.nomask)
            u = u_old
            v = v_old            

            """Multi-pass""" 
            
            for k in range(1, settings.num_iterations):
                                           
                x, y, u, v, sig2noise, mask = windef.multipass_img_deform(frame1.astype(np.int32),
                                                                            frame2.astype(np.int32),
                                                                            dt,
                                                                            k,
                                                                            x, y, u, v,
                                                                            settings,
                                                                            [])
                
            
                #u = np.ma.asarray(u,np.ma.nomask)
                #v = np.ma.asarray(v,np.ma.nomask)
                
            
            velocity_field[i] = {'x':x,'y':y,'u':u,'v':v,'mask':mask}
        
            vectu = np.append(vectu, u)
            vectv = np.append(vectv, v)
            Clock.schedule_once(partial(self.update_bar,i/nbFramOfInterest))
            
        self.popup.dismiss()
        np.save('velocity.npy',velocity_field)
        
        #save velocity informations in a text file
        listotal = [vectu, vectv]
        f=open('Velocity.txt','w')
        f.write('u,v ')
        f.write("\n")
        np.savetxt(f, list(zip(*listotal)), delimiter=',')
        f.close()
        
        info = {}
        info['ROI'] = app.ROI
        info['mask'] = app.IMGMASKS

        np.save('maskandroi.npy',info)
        vid.release()
        # computation of the mean velocity field using the computeMeanVelocity function
        # of the meansVelocity.py file
        (x,y,u_mean,v_mean) = computeMeanVelocity(self.img)
        
        app.MEANVELOCITYDATA['x'] = x
        app.MEANVELOCITYDATA['y'] = y
        app.MEANVELOCITYDATA['u_mean'] = u_mean
        app.MEANVELOCITYDATA['v_mean'] = v_mean
        # display the mean velocity field
        self.ids.VelocityGraphID.clear_widgets()
        fig, ax = plt.subplots()
        ax = plt.gca()
        ax.set_facecolor('#33333d')
        fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(self.img, cmap='gray')
        plt.draw()
        ax.quiver(x, y, u_mean, v_mean, color='orange',width=0.001)    
        widget = FigureCanvasKivyAgg(fig)
        self.ids.VelocityGraphID.add_widget(widget)

        
## SECTION OF INTEREST SCREEN 


class SectionOfInterest(Screen):  
    
    """ Selection of the section of interest where discharge will be computed """
    
    def on_enter(self):
        app = App.get_running_app()
        self.ids.RectifiefGraphID.clear_widgets()
        if app.ORTHO == True:
            self.img = app.ORTHOPARAMS['img_rectified']
        else:
            vid = cv2.VideoCapture(app.VIDEOFILEPATH)
            ret, frame = vid.read()
            vid.release()
            if len(app.ROI) == 4:
                self.img =  frame[app.ROI[0]:app.ROI[1],app.ROI[2]:app.ROI[3]]
            else:
                self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(self.img,cmap='gray')
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.RectifiefGraphID.add_widget(widget)
        self.fig.canvas.mpl_connect('button_press_event',self.onclick)
    
        
        self.pts_section = []
        
        self.line2, = self.ax.plot(self.pts_section[::2],self.pts_section[1::2], 'r.',markersize=15)
        
        self.choiceSectPts = False
        
    def onclick(self,event):

        if self.choiceSectPts:
            x, y = event.inaxes.transData.inverted().transform((event.x, event.y))
            self.pts_section  += [x, y]
            self.line2.set_xdata(self.pts_section[::2])
            self.line2.set_ydata(self.pts_section[1::2])
            self.fig.canvas.draw()    
        
    def selectSectPoints(self):
        self.choiceSectPts = True
        self.pts_section = []
        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        self.fig.canvas.draw()
    
        
    def saveInformation(self):
        self.line2.set_xdata(np.array([]))
        self.line2.set_ydata(np.array([]))
        plt.plot(self.pts_section[::2],self.pts_section[1::2],'b.', markersize=15)
        self.fig.canvas.draw()
        self.pts_section = np.array(list(zip(self.pts_section[::2],self.pts_section[1::2])))
        
        #print(self.pts_section)
        #self.pts_section = np.array([[122.97816524, 614.74947779], [815.58977898, 634.29024433]])
        
        app = App.get_running_app()
        
        if app.ORTHO == False:
            L_pixel = np.sqrt((self.pts_section[1,0] - self.pts_section[0,0])**2 + \
                  (self.pts_section[1,1] - self.pts_section[0,1])**2) #used for to calculate the scalingFactorWithoutOrtho
            L_real = findLength(app.BATHFILEPATH,app.WATERLEVEL)
            print('Largeur calculee sans orthorectification, à partir du niveau d eau :', L_real)
            self.scaling_factorWithoutOrtho = L_pixel/L_real
            print('Infos: The calculated scaling factor without orthorectification is ', self.scaling_factorWithoutOrtho)
            app.SECTIONINTERESTDATA['scalingFactorWithoutOrtho'] = self.scaling_factorWithoutOrtho
            
        self.img_rotated, self.angle_rotation = rotation(self.img, self.pts_section)
        
        app = App.get_running_app()

        app.SECTIONDATA['pts_section'] = self.pts_section
        app.SECTIONDATA['img_rotated'] = self.img_rotated
        app.SECTIONDATA['angle_rotation'] = self.angle_rotation
        
        
class NbSubsectionPopup(Popup):
    
    """ Popup that ask the number of subsections and so velocity vectors
        the user wants """
    SetNbSubSect = ObjectProperty()
    

class RetrievSectionVelocityVectors(Screen):
    
    """ Retrieve of the velocity vectors on the section chosen """
    
    def SetNbSubSect(self, nb):
        self.nbSubSection = nb
        self.saveInformation()

        
    def on_enter(self):
        self.popup = NbSubsectionPopup(SetNbSubSect = self.SetNbSubSect)
        self.popup.open()
        app = App.get_running_app()
        
        pts_section = app.SECTIONDATA['pts_section']
        self.img_rotated = app.SECTIONDATA['img_rotated']
        self.angle_rotation = app.SECTIONDATA['angle_rotation']
        
        if app.ORTHO == True:
            
            self.img, self.h, self.Xmin, self.Ymin, self.scaling_factor = app.ORTHOPARAMS['img_rectified'],app.ORTHOPARAMS['h'], app.ORTHOPARAMS['Xmin'], app.ORTHOPARAMS['Ymin'], app.ORTHOPARAMS['scaling_factor']
            # function of homography file
            _ , inside_roi = selectionSection(pts_section, self.angle_rotation, self.h, self.Xmin, self.Ymin)
            # Check if the section is inside the ROI chosen earlier
            print(inside_roi)
        else:
           #self.img = app.IMG
           self.img = self.img_rotated #changement par rapport à la ligne d'avant, car mauvais affichage de la largeur
        
        self.ids.SectionGraphID.clear_widgets()
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(self.img_rotated,cmap='gray')
        rot_mat = np.array([[math.cos(self.angle_rotation),math.sin(self.angle_rotation)],
                        [-math.sin(self.angle_rotation), math.cos(self.angle_rotation)]])
        rot_imgCenter = (np.array(self.img_rotated.shape[:2][::-1])-1)/2
        org_imgCenter = (np.array(self.img.shape[:2][::-1])-1)/2
    
        self.pts_sectionRot = np.dot(pts_section-org_imgCenter, rot_mat.T) + rot_imgCenter
        
        
        plt.plot(self.pts_sectionRot[:,0], self.pts_sectionRot[:,1], 'k-', linewidth=2, zorder=1)
        plt.plot(self.pts_sectionRot[:,0], self.pts_sectionRot[:,1], 'r.', markersize=10, zorder=2)
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.SectionGraphID.add_widget(widget)
        
    def saveInformation(self):
        app = App.get_running_app()
        x = app.MEANVELOCITYDATA['x']
        y = app.MEANVELOCITYDATA['y']
        u_mean = app.MEANVELOCITYDATA['u_mean']
        v_mean = app.MEANVELOCITYDATA['v_mean']
        ROI = app.ROI
        
        # Use of the function inside the RiverFlowComputation.py file to 
        # retrieve the velocity vectors on the section of interest
        if app.ORTHO == True:
            img = app.ORTHOPARAMS['img']
            self.x_interest, self.y_interest, self.u_interest, self.v_interest = retrieveSectionInformation(x, y, u_mean, v_mean, ROI, self.img, self.img_rotated,
                                self.pts_sectionRot, self.Xmin, self.Ymin, self.h, self.angle_rotation, self.nbSubSection)           
        else :
            img = app.IMG
            self.x_interest, self.y_interest, self.u_interest, self.v_interest = retrieveSectionInformationWithoutOrtho(x, y, u_mean, v_mean, ROI, self.img,
                       self.pts_sectionRot, self.nbSubSection, self.img_rotated, self.angle_rotation)
        
    
        data = np.loadtxt(app.BATHFILEPATH, delimiter = ',')
        xbath = np.array(data[:,0])
        ybath = np.array(data[:,1])
        level_water = app.WATERLEVEL
        # Use of the function inside the RiverFlowComputation.py file to 
        # compute the area in each subsection
        self.area, self.x_area, self.y_area = computeAreaSection(xbath, ybath, level_water, self.nbSubSection)
                
        app.SECTIONINTERESTDATA['x'] = self.x_interest
        app.SECTIONINTERESTDATA['y'] = self.y_interest
        app.SECTIONINTERESTDATA['u'] = self.u_interest
        app.SECTIONINTERESTDATA['v'] = self.v_interest 
        app.SECTIONINTERESTDATA['nbSubSection'] = self.nbSubSection
        app.SECTIONINTERESTDATA['area'] = self.area
        app.SECTIONINTERESTDATA['x_area'] = self.x_area
        app.SECTIONINTERESTDATA['y_area'] = self.y_area
        
    def showVelocityVector(self):
        self.ids.SectionGraphID.clear_widgets()
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        plt.imshow(self.img_rotated,cmap='gray')
        plt.plot(self.pts_sectionRot[:,0], self.pts_sectionRot[:,1], 'k-', linewidth=2, zorder=1)
        plt.plot(self.x_interest, self.y_interest, 'g.', markersize=5, zorder=2)
        plt.plot(self.pts_sectionRot[:,0], self.pts_sectionRot[:,1], 'r.', markersize=10, zorder=3)
        self.ax.quiver(self.x_interest, self.y_interest, self.u_interest, self.v_interest, color='orange',width=0.005,angles='xy')
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.SectionGraphID.add_widget(widget)

class CoefficientVelocityPopup(Popup):
    """ Popup to get the velocity index value  """
    compute = ObjectProperty()
    setCoef = ObjectProperty()
    
#class PointsNotFound(Popup):
    #pass

## DISCHARGE COMPUTATION SCREEN

class DischargeComputation(Screen):       
    
    """ Screen that deals with the computation of the discharge """
    
    def on_enter(self):
        self.p = CoefficientVelocityPopup(compute=self.compute, setCoef = self.setCoef)
        self.p.open()
        app = App.get_running_app()
        self.x_area = app.SECTIONINTERESTDATA['x_area']
        self.y_area = app.SECTIONINTERESTDATA['y_area']
        nbSubSection = app.SECTIONINTERESTDATA['nbSubSection']
        
        self.ids.DischargeGraphID.clear_widgets()
        self.fig, self.ax = plt.subplots()
        self.ax.set_facecolor('#33333d')
        self.fig.patch.set_facecolor('#33333d')
        plt.axis('off')
        self.ax.set_title('Area considered in each subsection',color='white', fontsize=20)
        for i in range(nbSubSection):
            plt.plot(self.x_area[i][1:-1], self.y_area[i][1:-1])

            plt.fill(self.x_area[i], self.y_area[i], edgecolor='k', alpha=0.2)
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.DischargeGraphID.add_widget(widget)
        
    def setCoef(self):
        app = App.get_running_app()
        data = np.loadtxt(app.BATHFILEPATH, delimiter = ',')
        ybath = np.array(data[:,1])

        # Rule of Hauet article below 0.2m of water level the coefficient should be 0.8 and 0.9 otherwise
        if (app.WATERLEVEL - min(ybath)) > 2:
            return '0.8'
        else:
            return '0.9'
        
    def compute(self, coefficient):
        # function where the discharge is computed using a function of the 
        # riverFlowComputation.py file
        app = App.get_running_app()
        self.v = app.SECTIONINTERESTDATA['v']
        self.area = app.SECTIONINTERESTDATA['area']
        if app.ORTHO:
            self.scaling_factor = app.ORTHOPARAMS['scaling_factor']
        else:
            self.scaling_factor = app.SECTIONINTERESTDATA['scalingFactorWithoutOrtho']
        self.coefficient = coefficient
        discharge = computeDischarge(self.v, self.coefficient, self.area, self.scaling_factor)
        self.ids.valID.text = f'{discharge:.4f} m\N{SUPERSCRIPT THREE}/s'
        
        
        x = app.MEANVELOCITYDATA['x']
        y = app.MEANVELOCITYDATA['y']
        u_mean = app.MEANVELOCITYDATA['u_mean'] 
        v_mean = app.MEANVELOCITYDATA['v_mean']
        np.save('analysisResults.npy',{'x':x,'y':y,'u_mean':u_mean,'v_mean':v_mean,'water_level':app.WATERLEVEL,'discharge':discharge})
        
        WL=str(app.WATERLEVEL)
        coefficient=str(coefficient)
        Q=str(discharge)
        
        #save final results in a textfile
        f=open('analysisResults.txt','w')
        f.write('x : ')
        np.savetxt(f, x, fmt='%1.3f', newline=", ")
        f.write("\n")
        f.write ('y : ')
        np.savetxt(f, y, fmt='%1.3f', newline=", ")
        f.write("\n")
        f.write ('u_mean : ')
        np.savetxt(f, u_mean, fmt='%1.3f', newline=", ")
        f.write("\n")
        f.write ('v_mean : ')
        np.savetxt(f, v_mean, fmt='%1.3f', newline=", ")
        f.write("\n")
        f.write('alpha : ')
        f.write(coefficient)
        f.write("\n")
        f.write('Waterlevel : ')
        f.write(WL)
        f.write (' m')
        f.write("\n")
        f.write('Discharge : ')
        f.write(Q)
        f.write(' m³/s')
        f.close()
        
        
class WindowManager(ScreenManager):
    pass

# loading of the kv file
kv = Builder.load_file('riverDischargeApplication.kv')

class Discharge_AnalysisApp(App):
    # global application variables
    IMG = np.array([])
    BATHFILEPATH = ''
    ORTHOPARAMS = {}
    SECTIONDATA = {}
    MEANVELOCITYDATA = {}
    SECTIONINTERESTDATA = {}
    WATERLEVEL = 0.0
    WATERLEVELPATH = ''
    CALIBRATIONFILE = ''
    VIDEOFILEPATH = ''
    IMGMASKS = np.array([])
    VIDEORANGE = [0,0]
    VIDEOSTEP = 1
    ROI = np.array([0])
    FILTERS = []
    FILTERSPARAM = []
    ORTHO = False
    CALIB = False
    
    def build(self):
        return kv
    
if __name__ =="__main__":
    Discharge_AnalysisApp().run()