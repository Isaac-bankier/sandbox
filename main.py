from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from PIL import Image

#Helper functions
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

def generateFrame():
    #initial setup
    depth = get_depth()[0]
    newDepth = []
    one = 0
    two = 0
    stride = 1

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
    print(len(depth))

    #rgb = get_video()
    my_list = []

    msd = drawing(marchingSquares(depth, 1000), (255, 255, 255), (255, 0, 0), (0, 0, 0))
    my_list = msd[0]
    width = msd[1]
    height = msd[2]

    #generates the image
    img = Image.new('RGB', (width, height))
    img.putdata(my_list)
    img.show()
    img.save('image.png')
