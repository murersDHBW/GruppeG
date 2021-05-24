import math
def degToPos(angle: float, length: float) -> list[float]:
    x = math.cos(angle) * length
    y = math.sin(angle) * length
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