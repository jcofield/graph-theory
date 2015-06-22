from __future__ import print_function

def mgColor(V,E,verbose=0):
    """
    Use Misra & Gries' algorithm to produce a proper coloring of the edges E
    :param V: (list) Vertex labels
    :param E: (list of 2-tuples) Each edge tuple consists of two vertices
    :param verbose: Use True for detailed output
    :return colors: (dict) Keys are edge tuples, where an edge tuple is represented as (i,j) with i<j.
    Values are colors, represented as integers from 1 to the maximum degree of G plus 1
    """

    #Construct the graph with no colors
    G = {v:[e[not i] for e in E for i in [0,1] if v==e[i]] for v in V}
    coloredG = {v:[] for v in G}
    uncoloredEdges = [tuple(sorted(e)) for e in E]
    edgeColors = {}
    colorsUsed = []

    #Misra Gries's Algorithm to iteratively color one new edge at a time
    while len(uncoloredEdges)>0:
        print("Finding two edges to color from %s uncolored edges"%len(uncoloredEdges))
        #Get next edge to color
        uVertex,vVertex = uncoloredEdges.pop()
        #Get maximal fan of uVertex that starts with vVertex
        maxFan,fanColors = getMaxFan(uVertex,vVertex,coloredG,edgeColors)
        checkProper(edgeColors,G)

        #Find a free color for the uVertex
        uAdjacentColors = [edgeColors[tuple(sorted([uVertex,vertex]))] for vertex in coloredG[uVertex]]
        if len(uAdjacentColors) == len(colorsUsed):
            uFreeColor = len(colorsUsed)
            colorsUsed.append(uFreeColor)
        else:
            for color in colorsUsed:
                if color not in uAdjacentColors:
                    uFreeColor = color
                    break
        checkProper(edgeColors,G)

        #Find a free color for the last fan element
        fanEndAdjacentColors = set([edgeColors[tuple(sorted([maxFan[-1],vertex]))] for vertex in coloredG[maxFan[-1]]])
        if set(fanEndAdjacentColors) == set(colorsUsed):
            fanEndFreeColor = len(fanEndAdjacentColors)
            colorsUsed.append(fanEndFreeColor)
        for color in colorsUsed:
            if color not in fanEndAdjacentColors:
                fanEndFreeColor = color
                break
        checkProper(edgeColors,G)

        #Invert the path of the two colors starting at uVertex
        invertPath(uFreeColor,fanEndFreeColor,uVertex,coloredG,edgeColors)
        for i in xrange(len(fanColors)):
            if fanColors[i] == fanEndFreeColor: fanColors[i]=uFreeColor
        checkProper(edgeColors,G)

        if uFreeColor not in fanColors:
            wVertex = maxFan[-1]
        else:
            #Todo: This edge can be found constructively from the proof, instead of iterating
            for v1 in maxFan:
                isFree = True
                for v2 in coloredG[v1]:
                    if edgeColors[tuple(sorted([v1,v2]))] == fanEndFreeColor:
                        isFree = False
                        break
                if isFree:
                    wVertex = v1
                    break

        subFan = maxFan[0:maxFan.index(wVertex)]
        checkProper(edgeColors,G)
        #Rotate the sub-fan of vVertex to wVertex then color the wVertex edge
        for vertex in [v for v in subFan if v!=wVertex]:
            nextVertex = maxFan[maxFan.index(vertex)+1]
            edgeColors[tuple(sorted([uVertex,vertex]))] = edgeColors[tuple(sorted([uVertex,nextVertex]))]
        edgeColors[tuple(sorted([uVertex,wVertex]))] = fanEndFreeColor
        checkProper(edgeColors,G)

        coloredG[uVertex].append(vVertex)
        coloredG[vVertex].append(uVertex)
        checkProper(edgeColors,G)
    return edgeColors

def checkProper(edgeColor,G):
    """
    Looks through the graph for vertices with two incident edges of the same color
    """
    isProper = True
    for v in G.keys():
        incidentEdgeColors = {edgeColor[tuple(sorted([v,i]))]:[] for i in G[v] if tuple(sorted([v,i]))
                  in edgeColor.keys()}
        for neighbor in [i for i in G[v] if tuple(sorted([v,i])) in edgeColor.keys()]:
            neighborColor = edgeColor[tuple(sorted([v,neighbor]))]
            incidentEdgeColors[neighborColor].append(neighbor)
            if len(incidentEdgeColors[neighborColor])>1:
                for vertex in incidentEdgeColors[neighborColor]:
                    print(edgeColor)
                    print("An improper coloring was found at vertex %s"%v)
                    print("The edge %s has color %s"%(sorted([v,vertex]),neighborColor))
                    isProper = False
    if not isProper:
        raise("ERROR")
    #TODO: A simplier way is to look at all edges with color k and check that no vertex appears twice

#Helper Functions
def getMaxFan(centerVertex,otherVertex,coloredG,edgeColor):
    """Find a maximal fan from a center vertex that starts at another given vertex"""
    fanOptions = coloredG[centerVertex][:]
    fan = [otherVertex]
    fanColors = ["None"]
    lastAdded = otherVertex
    maximal = len(fanOptions)==0
    while not maximal:
        maximal=True
        badColors = [edgeColor[tuple(sorted([lastAdded,vertex]))] for vertex in coloredG[lastAdded]]
        for vertex in fanOptions:
            if edgeColor[tuple(sorted([centerVertex,vertex]))] not in badColors:
                fan.append(vertex)
                fanColors.append(edgeColor[tuple(sorted([centerVertex,vertex]))])
                fanOptions.remove(vertex)
                lastAdded = vertex
                maximal=False
                break
    return fan,fanColors

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