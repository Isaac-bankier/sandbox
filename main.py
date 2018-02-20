from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from PIL import Image
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class sandbox(object):
    def __init__(self, colourScale):
        self.colourScale = colourScale
        self.depthCache = None
        self.imageCache = None

    def generateColour(self, percent):
        if percent==0.0:
            return self.colourScale[0][1]
        if percent==1.0:
            return self.colourScale[len(self.colourScale)-1][1]

        for c in range(len(self.colourScale)):
            if self.colourScale[c][0] < percent:
                r = int((float(self.colourScale[c][1][0]  - float(self.colourScale[c-1][1][0])) * percent) + float(self.colourScale[c-1][1][0]))
                g = int((float(self.colourScale[c][1][1]  - float(self.colourScale[c-1][1][1])) * percent) + float(self.colourScale[c-1][1][1]))
                b = int((float(self.colourScale[c][1][2]  - float(self.colourScale[c-1][1][2])) * percent) + float(self.colourScale[c-1][1][2]))
                a = int((float(self.colourScale[c][1][3]  - float(self.colourScale[c-1][1][3])) * percent) + float(self.colourScale[c-1][1][3]))
                return (r, g, b, a)

    def logger(self, message, level=1):
        front=""
        if level ==0:
            #Debug
            front="\033[0;37m[0]\033[0;37m "
        if level ==1:
            #Info
            front="\033[0;34m[+]\033[0;37m "
        if level ==2:
            #Warning
            front="\033[0;33m[-]\033[0;37m "
        if level ==3:
            #Error
            front="\033[0;31m[*]\033[0;37m "
        if level ==4:
            #Fatal
            front="\033[7;31m[!] "

        print(front+message+"\033[0;37m")

    def lookup(self, a, b, c, d):
        if a:
            if b:
                if c:
                    if d:
                        return 0
                    else:
                        return 2
                else:
                    if d:
                        return 1
                    else:
                        return 3
            else:
                if c:
                    if d:
                        return 4
                    else:
                        return 6
                else:
                    if d:
                        return 5
                    else:
                        return 7
        else:
            if b:
                if c:
                    if d:
                        return 8
                    else:
                        return 10
                else:
                    if d:
                        return 9
                    else:
                        return 11
            else:
                if c:
                    if d:
                        return 12
                    else:
                        return 14
                else:
                    if d:
                        return 13
                    else:
                        return 15

    def marchingSquares(self, points, thresh):
        newPoints = []

        # check if points are above the thresh hold and add values to new points
        for h in points:
            newLine = []
            for w in h:
                if w >= thresh:
                    newLine.append(True)
                else:
                    newLine.append(False)
            newPoints.append(newLine)

        contours=[]
        for h in range(len(newPoints)-1):
            newLine = []
            for w in range(len(newPoints[h])-1):
                a = newPoints[h][w]
                b = newPoints[h][w+1]
                c = newPoints[h+1][w]
                d = newPoints[h+1][w+1]
                newLine.append(self.lookup(a, b, c, d))
            contours.append(newLine)

        return contours

    def drawSquare(self, type, c1, c2, c3):
        pass

    def singleSquare(self, p1, p2, p3, p4, thresh, c1=(0, 0, 0, 0), c2=(0, 0, 0, 255), c3=(255, 255, 255, 255)):
        images = [[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c2, c3, c3, c3, c3, c3, c3, c3, c3, c3, c1, c2, c3, c3, c3, c3, c3, c3, c3, c3, c1, c1, c2, c3, c3, c3, c3, c3, c3, c3, c1, c1, c1, c2, c3, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c2, c3, c3, c3, c3, c3, c3, c3, c3, c2, c1, c3, c3, c3, c3, c3, c3, c3, c2, c1, c1, c3, c3, c3, c3, c3, c3, c2, c1, c1, c1, c3, c3, c3, c3, c3, c2, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c3, c2, c1, c1, c1, c1, c3, c3, c3, c3, c3, c3, c2, c1, c1, c1, c3, c3, c3, c3, c3, c3, c3, c2, c1, c1, c3, c3, c3, c3, c3, c3, c3, c3, c2, c1, c3, c3, c3, c3, c3, c3, c3, c3, c3, c2, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c2, c1, c1, c1, c1, c1, c1, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c3, c2, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c2, c3, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c1, c1, c1, c1, c1, c1, c2, c3, c3, c3, c1, c1, c1, c1, c1, c2, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c2, c1, c1, c1, c1, c1, c1, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c3, c2, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c2, c3, c3, c3, c3, c3, c3, c1, c1, c2, c3, c3, c3, c3, c3, c3, c3, c1, c2, c3, c3, c3, c3, c3, c3, c3, c3, c2, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c1, c2, c3, c3, c3, c3, c1, c1, c1, c1, c1, c1, c2, c3, c3, c3, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c3, c3, c3, c2, c1, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3, c1, c1, c1, c1, c1, c2, c3, c3, c3, c3, c1, c1, c1, c1, c1, c1, c2, c3, c3, c3, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c1, c1, c1, c1, c1, c1, c1, c1, c2, c3, c1, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c2, c3, c1, c1, c1, c1, c1, c1, c1, c2, c3, c3, c1, c1, c1, c1, c1, c1, c2, c3, c3, c3, c1, c1, c1, c1, c1, c2, c3, c3, c3, c3, c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c2, c1, c1, c1, c1, c1, c1, c1, c1, c1, c3, c2, c1, c1, c1, c1, c1, c1, c1, c1, c3, c3, c2, c1, c1, c1, c1, c1, c1, c1, c3, c3, c3, c2, c1, c1, c1, c1, c1, c1, c3, c3, c3, c3, c2, c1, c1, c1, c1, c1, c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]

        if p1 > thresh:
            p1=True
        else:
            p1=False

        if p2 > thresh:
            p2=True
        else:
            p2=False

        if p3 > thresh:
            p3=True
        else:
            p3=False

        if p4 > thresh:
            p4=True
        else:
            p4=False

        img = Image.new('RGBA', (10, 10))
        img.putdata(images[self.lookup(p1, p2, p3, p4)])
        return img

    def drawing(self, contour, c1, c2, c3):
        #c1 under colour
        #c2 line colour
        #c3 upper colour
        pixelArray = []
        height = len(contour)*10
        width = len(contour[0])*10

        images = [[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c2, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c2, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c2, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c2, c1],[c3, c3, c3, c3, c3, c3, c3, c2, c1, c1],[c3, c3, c3, c3, c3, c3, c2, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c2, c2, c2, c2, c2, c2, c2, c2, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c3, c2, c1, c1, c1],[c3, c3, c3, c3, c3, c3, c3, c2, c1, c1],[c3, c3, c3, c3, c3, c3, c3, c3, c2, c1],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c2, c3, c3, c3, c3, c3, c3],[c1, c1, c2, c3, c3, c3, c3, c3, c3, c3],[c1, c2, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c2, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c2],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c2, c2, c2, c2, c2, c2, c2, c2, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]]]

        for h in contour:
            for i in range(0, 10):
                for w in h:
                    for p in images[w][0][i]:
                        pixelArray.append(p)

        return (pixelArray, width, height)

    def generateSingleLayer(self, interval, depth, c1=(0, 0, 0, 0), c2=(0, 0, 0, 255), c3=(255, 255, 255, 255)):
        #initial setup
        self.logger("Setup", 0)

        #rgb = get_video()
        my_list = []
        self.logger("Drawing...", 0)
        msd = self.drawing(self.marchingSquares(depth, interval), c1, c2, c3)
        my_list = msd[0]
        width = msd[1]
        height = msd[2]

        #generates the image
        self.logger("Generating...", 0)
        img = Image.new('RGBA', (width, height))
        img.putdata(my_list)
        self.logger("Done...", 0)
        print()
        return img

    def generateSingleFrame(self, interval, start, end, stride=8):
        depth = get_depth()[0]
        depth = self.adjustDepth(depth, stride)
        self.depthCache = depth
        layers = []
        for i in range(start, end, interval):
            layers.append(self.generateSingleLayer(i, depth, c3=self.generateColour((float(i)/(float(end)-float(start))))))

        for i in range(1, len(layers)):
            layers[0].paste(layers[i], (0, 0), layers[i])
        layers=layers[0]
        self.imageCache = layers
        return layers

    def adjustDepth(self, depth, stride):
        #lower resolution of array
        newDepth = []
        one = 0
        two = 0
        for h in depth:
            one += 1
            if one % stride != 0:
                continue

            else:
                line = []
                for w in h:
                    two += 1
                    if two % stride != 0:
                        continue

                    else:
                        line.append(w)

                newDepth.append(line)
        return newDepth

    def resolveDeltas(self, depth, cache, deltaThreshold):
        refreshPoints=[]
        self.logger("Resolving deltas ", 3)
        for h in range(len(depth)):
            for w in range(len(depth[0])):
                if abs(float(depth[h][w]) - float(cache[h][w])) < float(deltaThreshold):
                    continue
                else:
                    refreshPoints.append((h, w))

        return refreshPoints

    def patchImage(self, interval, start, end, stride=8, deltaThreshold=10):
        depth = get_depth()[0]
        depth = self.adjustDepth(depth, stride)
        oldDepth = self.depthCache
        self.depthCache = depth
        patchedImage = self.imageCache

        changes = self.resolveDeltas(depth, oldDepth, deltaThreshold)
        newSquares = set()
        self.logger(str(len(changes))+" deltas", 3)
        for c in changes:
            #top left square
            try:
                newSquares.add((((c[1]-1)*10, (c[0]-1)*10), (depth[c[0]-1][c[1]-1], depth[c[0]-1][c[1]], depth[c[0]][c[1]-1], depth[c[0]][c[1]])))
            except IndexError:
                continue

            #top right square
            try:
                newSquares.add(((c[1]*10, (c[0]-1)*10), (depth[c[0]-1][c[1]], depth[c[0]-1][c[1]+1], depth[c[0]][c[1]], depth[c[0]][c[1]+1])))
            except IndexError:
                continue

            #bottom left square
            try:
                newSquares.add((((c[1]-1)*10, c[0]*10), (depth[c[0]][c[1]-1], depth[c[0]][c[1]], depth[c[0]+1][c[1]-1], depth[c[0]+1][c[1]])))
            except IndexError:
                continue

            #bottom right square
            try:
                newSquares.add(((c[1]*10, c[0]*10), (depth[c[0]][c[1]], depth[c[0]][c[1]+1], depth[c[0]+1][c[1]], depth[c[0]+1][c[1]+1])))
            except IndexError:
                continue

        self.logger("Drawing", 3)
        for i in range(start, end, interval):
            for square in newSquares:
                patchSquare = self.singleSquare(square[1][0], square[1][1], square[1][2], square[1][3], i, c3=self.generateColour((float(i)/(float(end)-float(start)))))
                patchedImage.paste(patchSquare, (square[0][0], square[0][1]), patchSquare)

        self.imageCache = patchedImage
        return patchedImage


#image server
class imageServer(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        #testing
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        #/testing
        return

def startImageServer(serverAddr, serverPort):
    # Server settings
    server_address = (serverAddr, serverPort)
    httpd = HTTPServer(server_address, imageServer)
    thread = threading.Thread(target=httpd.serve_forever, args=())
    thread.start()
    serverLocation = "http://"+serverAddr + ':' + str(serverPort)
    return serverLocation


    colourScale=[[0.0, (166,206,227,255)], [0.25, (31,120,180,255)], [0.45, (178,223,138,255)], [0.65, (51,160,44,255)], [0.85, (251,154,153,255)], [1.0, (227,26,28,255)]]
    s=sandbox(colourScale)

    #import cProfile
    #cProfile.run('s.generateSingleFrame(25, 0, 1000).save("test.png")')
    s.generateSingleFrame(100, 0, 1000, stride=8).save("test.png")
    while True:
        dt = datetime.now()
        s.patchImage(100, 0, 1000, stride=8, deltaThreshold=20).save("test2.png")
        dt2 = datetime.now()
        s.logger(str(float(dt2.microsecond - dt.microsecond)/1000000.0), 4)
