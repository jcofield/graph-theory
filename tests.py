import random
from mgColor import *

# Test full algorithm on a small graph
vertices = [0,1,2,3,4,100,200,300,400,101,201,301,401]
edges = [(0,2),(0,3),(0,4)] + [(1,100),(1,101)]+ [(2,200),(2,201)] + [(3,300),(3,301)] + [(4,400),(4,401)]
colorsOfGraph = mgColor(vertices,edges)
print("Final coloring: %s"%colorsOfGraph) #Easy to check that this is proper by inspection
print("--------------------------------------------------------------")

# Test full algorithm on a random graph
vertices = range(0,100)
#Randomly connect 1/34 of all possible edges
edges = [(i,j) for i in vertices for j in vertices if i<j if not random.randrange(35)]
colorsOfGraph = mgColor(vertices,edges)
print("Final coloring: %s"%colorsOfGraph)
print("--------------------------------------------------------------")

# Test 1
print("Testing invertPath function")
G = {0:[2,3,4],1:[100,101],2:[0,200,201],3:[0,300,301],4:[0,400,401],100:[1],200:[2],300:[3],400:[4]}
color = {(1,100):"Red",(1,101):"Green",(0,2):"Blue",(2,200):"Red",(2,201):"Purple",(0,3):"Purple",(3,300):"Red",
         (3,301):"Green",(0,4):"Red",(4,400):"Green",(4,401):"Purple"}
for key in color.keys():
   color[(key[1],key[0])] = color[key]
print(color)
invertPath("Red","Green",0,G,color)
print(color)
print("The colors of edges (0,4) and (4,400) should be switched")
print("--------------------------------------------------------------")

#Test 2: Test inversions works
print("Testing invertPath function")
G = {0:[1,5],1:[0,2],2:[1,3],3:[2,4],4:[3],5:[0]}
color = {(0,1):"Red",(1,2):"Blue",(2,3):"Red",(3,4):"Blue",(0,5):"Purple"}
path = color.items()
path.sort()
print("BEFORE")
for edge in path:
   print("%s-%s: %s"%(edge[0][0],edge[0][1],edge[1]))
invertPath("Red","Blue",0,G,color)
print("AFTER")
path = color.items()
path.sort()
for edge in path:
   print("%s-%s: %s"%(edge[0][0],edge[0][1],edge[1]))
print("All red's and blue's should be switched")
print("--------------------------------------------------------------")

#Test 3: Test getMaxfan()
print("Testing the getMaxFan funtion")
color = {(0,2):"Red",(0,3):"Blue",(0,4):"Purple",(0,15):"Grey",(1,100):"Grey",(1,101):"Purple",(2,200):"Grey",(2,201):"Purple",(3,300):"Grey",(3,301):"Purple",(3,302):"Red",(4,400):"Grey",(1000,1001):"Gold"}
vertices = set([1,1000,1001]+[edge[0] for edge in color.keys()]+[edge[1] for edge in color.keys()])
G = {v:sorted([e[not i] for e in color for i in [0,1] if v==e[i]]) for v in vertices}
coloredG = G.copy()
gcolor = color.items()
gcolor.sort()
maxFan,fanColors= getMaxFan(0,1,coloredG,color)
gcolor = color.items()
gcolor.sort()
print("The colors of the graph are:")
for edge in gcolor:
   print("%s-%s: %s"%(edge[0][0],edge[0][1],edge[1]))
print("Fan: %s"%maxFan)
print("Therefore [1,2,3] is a maxFan")
