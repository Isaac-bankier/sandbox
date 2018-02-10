from PIL import Image

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

def marchingSquares(points, threash):

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
    height = len(contour)
    width = len(contour[0])

    images = [[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c2, c3, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c2, c3, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c2, c3, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c2, c1],[c3, c3, c3, c3, c3, c3, c3, c2, c1, c1],[c3, c3, c3, c3, c3, c3, c2, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c2, c2, c2, c2, c2, c2, c2, c2, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c3, c2, c1, c1, c1],[c3, c3, c3, c3, c3, c3, c3, c2, c1, c1],[c3, c3, c3, c3, c3, c3, c3, c3, c2, c1],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1]]],[[[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c2, c3, c3, c3, c3, c3, c3],[c1, c1, c2, c3, c3, c3, c3, c3, c3, c3],[c1, c2, c3, c3, c3, c3, c3, c3, c3, c3],[c2, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c2, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c2],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c2, c2, c2, c2, c2, c2, c2, c2, c2],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3],[c3, c3, c3, c3, c3, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c2],[c1, c1, c1, c1, c1, c1, c1, c1, c2, c3],[c1, c1, c1, c1, c1, c1, c1, c2, c3, c3],[c1, c1, c1, c1, c1, c1, c2, c3, c3, c3],[c1, c1, c1, c1, c1, c2, c3, c3, c3, c3],[c1, c1, c1, c1, c2, c3, c3, c3, c3, c3]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c2, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c3, c2, c1, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c2, c1, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c2, c1, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c2, c1, c1, c1, c1, c1],[c3, c3, c3, c3, c3, c2, c1, c1, c1, c1]]],[[[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1],[c1, c1, c1, c1, c1, c1, c1, c1, c1, c1]]]]

    for h in contour:
        for i in range(0, 10):
            for w in h:
                for p in images[w][i]:
                    pixelArray.append(p)

    return (pixelArray, width, height)
