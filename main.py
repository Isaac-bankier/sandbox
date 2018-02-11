from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from PIL import Image

#Helper functions
def generateColour(c1, c2, percent):
    r = int((float(c2[0] - c1[0]) * percent) + float(c1[0]))
    g = int((float(c2[1] - c1[1]) * percent) + float(c1[1]))
    b = int((float(c2[2] - c1[2]) * percent) + float(c1[2]))
    a = int((float(c2[3] - c1[3]) * percent) + float(c1[3]))
    return (r, g, b, a)

def logger(message, level=1):
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

def lookup(a, b, c, d):
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

def marchingSquares(points, thresh):
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
            newLine.append(lookup(a, b, c, d))
        contours.append(newLine)

    return contours

def drawing(contour, c1, c2, c3):
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

def generateSingleLayer(interval, depth,  stride=1, c1=(0, 0, 0, 0), c2=(255, 0, 0, 255), c3=(255, 255, 255, 255)):
    #initial setup
    logger("Setup", 0)
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

    depth = newDepth
    logger("Modified resolution", 0)
    print(len(depth))

    #rgb = get_video()
    my_list = []
    logger("Drawing...", 0)
    msd = drawing(marchingSquares(depth, interval), c1, c2, c3)
    my_list = msd[0]
    width = msd[1]
    height = msd[2]

    #generates the image
    logger("Generating...", 0)
    img = Image.new('RGBA', (width, height))
    img.putdata(my_list)
    logger("Done...", 0)
    print()
    return img

def generateSingleFrame(interval, start, end):
    depth = get_depth()[0]
    layers = []
    for i in range(start, end, interval):
        layers.append(generateSingleLayer(i, depth, stride=8, c2=(0, 0, 0, 255), c3=generateColour((255, 15, 0, 255), (0, 15, 255, 255), (i/(end-start)))))

    for i in range(1, len(layers)):
        layers[0].paste(layers[i], (0, 0), layers[i])

    return layers[0]

generateSingleFrame(25, 0, 1000).show()
