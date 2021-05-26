import math
def degToPos(angle: float, length: float) -> list[float]:
    y = math.cos(angle * (2 * math.pi / 360)) * length
    x = math.sin(angle * (2 * math.pi / 360)) * length
    return [x,y]

def vectorAddition(v1:list[float], v2:list[float]) -> list[float]:
    x = v1[0] + v2[0]
    y = v1[1] + v2[1]
    return [x,y]

def buildSVG(wallList: list[list[float]]) -> None:
    with open("wallList.svg", "a+") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
                    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="-1000 -1000 1000 1000">""")
        for wallPos in wallList:
            f.write('<circle cx="' + str(wallPos[0]/10) + '" cy="' + str(wallPos[1]/10) + '" r="2" fill="black"/>')
        f.write('</svg>')

def posToDeg(x,y):
    if x == 0 and y >= 0:
        return 90
    if x == 0 and y < 0:
        return 270
    if x < 0:
        return math.atan(y/x) + math.pi
    if y < 0:
        return math.atan(y/x) + 2 * math.pi
    return math.atan(y/x)

def get_mid_coord(v1,v2):
    x = (v1[0] + v2[0])/2
    y = (v1[1] + v2[1])/2
    return [x,y]

def euclidean_distance(v1,v2):
    return math.sqrt((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)


def get_next_pos(rawData, current_position):
    cleanData = []
    for i in range(len(rawData)-1):
        if not rawData[i+1][1] == rawData[i][1]:
            if rawData[i][1] < 750:
                cleanData.append(rawData[i])

    current_surrounding = []
    for x in cleanData:
        current_surrounding.append(vectorAddition(degToPos(x[0],x[1]-230),current_position))
    #x = [elem[0] for elem in deg]
    #y = [elem[1] for elem in deg]

    dist = []
    for i in range(len(deg)-1):
        dist.append(cleanData[i+1][0]-cleanData[i][0])
        #dist.append(euclidean_distance(deg[i+1],deg[i]))
    dist.append(cleanData[0][0]-cleanData[-1][0]+360)
    print(cleanData)
    #dist.append(euclidean_distance(deg[-1],deg[0]))
    v_index = dist.index(max(dist))

    if v_index+1 == len(dist):
        v_next = 0
    else:
        v_next = v_index+1
    if cleanData[v_index][0] > 180 and cleanData[v_next][0] <= 180:
        cleanData[v_index][0] = cleanData[v_index][0] - 360
    angle_next_pos = (cleanData[v_index][0] + cleanData[v_next][0])/2

    if angle_next_pos > 180:
        angle_next_pos -= 360
    return(angle_next_pos, current_surrounding)