from __future__ import print_function

def invertPath(color1,color2,start,coloredG,edgeColor):
    #Switches the colors of adjacent edges in a single path
    def switchColors(vertex1,vertex2):
        #Switch the color of a given edge
        if edgeColor[tuple(sorted([vertex1,vertex2]))] == color1: newColor = color2
        elif edgeColor[tuple(sorted([vertex1,vertex2]))] == color2: newColor = color1
        edgeColor[tuple(sorted([vertex1,vertex2]))] = newColor
    currentVertex = start
    lastVertex = start
    isMorePath = True
    while isMorePath:
        isMorePath = False
        for tryVertex in [v for v in coloredG[currentVertex] if v!=lastVertex]:
            if edgeColor[tuple(sorted([currentVertex,tryVertex]))] in [color1,color2]:
                switchColors(currentVertex,tryVertex)
                isMorePath = True
                lastVertex = currentVertex
                currentVertex = tryVertex
                break
