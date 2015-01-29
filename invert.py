from __future__ import print_function

def invertPath(color1,color2,start,coloredG,edgeColor):
    def switchColors(vertex1,vertex2):
        if edgeColor[(vertex1,vertex2)] == color1: newColor = color2
        elif edgeColor[(vertex1,vertex2)] == color2: newColor = color1
        edgeColor[(vertex1,vertex2)] = newColor
        edgeColor[(vertex2,vertex1)] = newColor
    currentVertex = start
    lastVertex = start
    isMorePath = True
    while isMorePath:
        isMorePath = False
        for tryVertex in [v for v in coloredG[currentVertex] if v!=lastVertex]:
            if edgeColor[currentVertex,tryVertex] in [color1,color2]:
                switchColors(currentVertex,tryVertex)
                isMorePath = True
                lastVertex = currentVertex
                currentVertex = tryVertex
                break

#Test
coloredG = {0:[2,3,4],1:[100,101],2:[0,200,201],3:[0,300,301],4:[0,400,401],100:[1],200:[2],300:[3],400:[4]}
color = {(1,100):"Red",(1,101):"Green",(0,2):"Blue",(2,200):"Red",(2,201):"Purple",(0,3):"Purple",(3,300):"Red",(3,301):"Green",(0,4):"Red",(4,400):"Green",(4,401):"Purple"}
for key in color.keys():
    color[(key[1],key[0])] = color[key]
print(color)
invertPath("Red","Green",0,coloredG,color)
print(color) #the edges (0,4) (4,0) (4,400) and (400,4) should have been switched