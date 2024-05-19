from FordFulkerson import *

print("="*16,"Inicio","="*16)
g = RedeDeFluxo()

vS = Vertice("S")
g.addVert(vS)
v1 = Vertice("v1")
g.addVert(v1)
v2 = Vertice("v2")
g.addVert(v2)
v3 = Vertice("v3")
g.addVert(v3)
v4 = Vertice("v4")
g.addVert(v4)
vT = Vertice("T")
g.addVert(vT)

g.AddAresta(vS,v1,16)
g.AddAresta(vS,v2,13)
g.AddAresta(v1,v3,12)
g.AddAresta(v2,v1,4)
g.AddAresta(v2,v4,14)
g.AddAresta(v3,v2,9)
g.AddAresta(v3,vT,20)
g.AddAresta(v4,v3,7)
g.AddAresta(v4,vT,4)


#print(g.FordFulkerson(vS,vT))
print("Fluxo máximo:",g.FordFulkersonCormen(vS,vT))
print("="*40)

g.plot_animation()
