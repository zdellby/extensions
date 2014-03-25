#CircleIFFT, by Zeno Dellby
#installed by putting it into a folder in the PlugIns directory,
#along with a file named __init__.py whose only contents are
#
#import CircleIFFT
#

import gettext

import numpy as np
import math

# local libraries
from nion.imaging import Image
from nion.imaging import Operation
from nion.swift import Application
_ = gettext.gettext  # for translation

#The operation class. Functions in it are called by Swift.
class CircleIFFTOperation(Operation.Operation):
    def __init__(self):
        super(CircleIFFTOperation, self).__init__(_("Circle IFFT"), "circle-ifft-operation")
        
    #This is called whenever Swift wants to update the Circle IFFT image
    def process(self, img):
        radius = min(img.shape[0],img.shape[1])/2
        w = max(512,radius*4) #the crop doesn't tell us what size the pre-cropped image would be
        grad = np.zeros((w,w),dtype=img.dtype) #work on an image of the larger size
        grad[(w - img.shape[0])/2:(w + img.shape[0])/2,(w - img.shape[1])/2:(w + img.shape[1])/2] = img[:,:] #put the FFT spot in the middle
        icol, irow = np.ogrid[0:w,0:w] #and now for making the circle:
        circle = np.zeros((w,w))
        circle = ((irow-w/2)**2 + (icol-w/2)**2) < radius**2
        grad = np.fft.ifft2(grad * circle)
        return grad #Return an image to Swift, because that's what it wants
        
    
#The following is code for making this into a process you can click on in the processing menu
 
def processing_circle_ifft(document_controller):
    document_controller.add_processing_operation_by_id("circle-ifft-operation", prefix=_("Circle IFFT of "))

def build_menus(document_controller): #makes the Show Circle IFFT Button
    document_controller.processing_menu.add_menu_item(_("Circle IFFT"), lambda: processing_circle_ifft(document_controller))

Application.app.register_menu_handler(build_menus) #called on import to make the Show Circle IFFT Button

Operation.OperationManager().register_operation("circle-ifft-operation", lambda: CircleIFFTOperation())
