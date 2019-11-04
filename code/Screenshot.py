 # * author : Philippe Vo 
 # * date : Oct-06-2019 14:17:38
 
# * Imports
# 3rd Party Imports
import pyscreenshot as ImageGrab
from pynput.mouse import Listener
import clipboard
import os
import sys
# User Imports

# * Code

class Screenshot():
    """
    screenshot grabber that will automatically save in the current directory under a name and return the save filepath for markdown
    """

    def __init__(self):
        """ inits. """
        self.x1 = 0 
        self.y1 = 0
        self.x2 = 0 
        self.y2 = 0

        self.firstClick = True

    # Mouse Functions
    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format("Pressed",(x,y)))

        if pressed and self.firstClick:
            self.x1 = x
            self.y1 = y
            self.firstClick = False
        elif pressed and not self.firstClick :
            self.x2 = x
            self.y2 = y
            return False
    
    def grab_screen(self):
        """ grab screen and returns the image """
        with Listener(on_click=self.on_click) as listener:
            listener.join()
        
        im = ImageGrab.grab(bbox=(self.x1, self.y1, self.x2, self.y2))  # X1,Y1,X2,Y2
        
        # save image file
        imageName = input("Filename : ")
        imageFileName = imageName +'.png'
        im.save(imageFileName)

        pathType = int(input("Would you like the relative or absolute path to file ? (1 : relative, 0 : absolute) : "))

        if pathType == 1:
            imageFilePath = os.path.relpath(imageFileName)
        elif pathType == 0:
            imageFilePath = os.path.realpath(imageFileName)
        else:
            print("invalid input")
            sys.exit()

        # Generating the markdown string 
        markdownStr = "![ Image : " + imageName + " ]" + "(" + imageFilePath + ")"
        # clipboard
        clipboard.copy(markdownStr)  # now the clipboard content will be string "abc"