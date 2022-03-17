## KIVY needed packages

from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.popup import Popup

## PYTHON needed packages

import numpy as np
import cv2
import glob
import os
import imutils
from imutils.video import FPS
import re
import math
import threading
from pathlib import Path
from functools import partial
from scipy import optimize, stats, ndimage
from scipy.signal import argrelextrema
# import skimage.external.tifffile as skiTif  # needed to read .tif file (used for DEM)
import tifffile as skiTif
#from openpiv import pyprocess, tools, validation, filters, scaling
import matplotlib.image as mpimg
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from openpiv import filters, smoothn, pyprocess, scaling, tools, validation, windef
#from openpiv import process
#import openpiv.gpu_process
#reload(openpiv.gpu_process)

## CUSTOM/CREATED functions 

from findIntersection import *
from parabolaVertex import *
from calibration import *
from filtersImage import *
from stabilization import *
from droneGeometryWaterLevel import *
from meansVelocity import *
from homography import *
from riverFlowComputation import *


"""
#openpiv en local
import filters
import pyprocess
import scaling
import tools
import validation
import windef
"""