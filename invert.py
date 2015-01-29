from __future__ import print_function

def invertPath(color1,color2,start,uninvertedG,edgeColor):
    for vertex in uninvertedG[start]:
        if edgeColor[start,vertex] in [color1,color2]:
            if edgeColor[start,vertex] == color1: edgeColor[start,vertex] = color2
            if edgeColor[start,vertex] == color2: edgeColor[start,vertex] = color1
            uninvertedG[start].remove(vertex)
            uninvertedG[vertex].remove(start)
            edgeColor,uninvertedG = invertPath(color1,color2,vertex,uninvertedG,edgeColor)
    return edgeColor,uninvertedG

#Test
coloredG = {0:[2,3,4],1:[100,101],2:[0,200,201],3:[0,300,301],4:[0,400,401],100:[1],200:[2],300:[3],400:[4]}
color = {(1,100):"Red",(1,101):"Green",(0,2):"Blue",(2,200):"Red",(2,201):"Purple",(0,3):"Purple",(3,300):"Red",(3,301):"Green",(0,4):"Red",(4,400):"Green",(4,401):"Purple"}
print(color)
color = invertPath("Red","Green",0,coloredG,color)
print(color)