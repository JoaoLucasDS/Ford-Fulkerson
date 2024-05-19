import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

class Vertice:
    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return f"{self.tag}"

class Aresta:
    def __init__(self, verticeEntr, verticeSaid, capacidade):
        self.verticeEntr = verticeEntr
        self.verticeSaid = verticeSaid
        self.capacidade = capacidade
        self.fluxo = 0

    def __repr__(self):
        return f"{self.verticeEntr.tag} -> {self.verticeSaid.tag}:{self.capacidade}"

class RedeDeFluxo:
    def __init__(self):
        self.listaVertices = {}
        self.fluxoMax = {}
        self.anim_data = []  # Data for animation
        self.vertice_anim_data = []  # Data for vertex animation

    def verificaVertice(self, vert):
        return isinstance(vert, Vertice)

    def addVert(self, vert):
        if self.verificaVertice(vert):
            self.listaVertices[vert] = []
            self.vertice_anim_data.append(('vertice', vert))
        else:
            print("Erro: Espera-se um Vertice")

    def listaAdj(self, vert):
        return self.listaVertices.get(vert)

    def AddAresta(self, verticeEntr, verticeSaid, capacidade=0):
        if self.verificaVertice(verticeEntr) and self.verificaVertice(verticeSaid):
            aresta = Aresta(verticeEntr, verticeSaid, capacidade)
            revAresta = Aresta(verticeSaid, verticeEntr, 0)

            aresta.duplicata = revAresta
            revAresta.duplicata = aresta

            self.listaVertices[verticeEntr].append(aresta)
            self.listaVertices[verticeSaid].append(revAresta)
            self.vertice_anim_data.append(('aresta', aresta))
        else:
            print("Erro: Espera-se uma Aresta entre dois Vertice")

    def Busca(self, origem, destino, caminho):
        if origem == destino:
            return caminho
        for aresta in self.listaAdj(origem):
            res = aresta.capacidade - self.fluxoMax[aresta]
            if res > 0 and not (aresta, res) in caminho:
                resultante = self.Busca(aresta.verticeSaid, destino, caminho + [(aresta, res)])
                if resultante:
                    return resultante

    def FordFulkersonCormen(self, s, t):
        print("Executando Ford-Fulkerson")
        for vert in self.listaVertices:
            for aresta in self.listaAdj(vert):
                self.fluxoMax[aresta] = 0
                self.fluxoMax[aresta.duplicata] = 0

        p = self.Busca(s, t, [])
        while p:
            fluxoPossivel = min(res for aresta, res in p)
            for aresta, res in p:
                self.fluxoMax[aresta] += fluxoPossivel
                self.fluxoMax[aresta.duplicata] -= fluxoPossivel

                self.anim_data.append((aresta.verticeEntr.tag, aresta.verticeSaid.tag, self.fluxoMax[aresta]))

            p = self.Busca(s, t, [])

        return sum(self.fluxoMax[aresta] for aresta in self.listaAdj(s))

    def plot_animation(self):
        G = nx.DiGraph()

        for vert in self.listaVertices:
            G.add_node(vert.tag)

        pos = nx.spring_layout(G)

        def update(frame):
            ax.clear()
            nx.draw(G, pos, ax=ax, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['fluxo']}/{d['capacity']}" for u, v, d in G.edges(data=True)}, ax=ax)

            if frame < len(self.vertice_anim_data):
                item_type, item = self.vertice_anim_data[frame]
                if item_type == 'vertice':
                    G.add_node(item.tag)
                elif item_type == 'aresta':
                    G.add_edge(item.verticeEntr.tag, item.verticeSaid.tag, capacity=item.capacidade, fluxo=0)
            else:
                anim_frame = frame - len(self.vertice_anim_data)
                if anim_frame < len(self.anim_data):
                    u, v, fluxo = self.anim_data[anim_frame]
                    if G.has_edge(u, v):
                        G[u][v]['fluxo'] = fluxo

        fig, ax = plt.subplots()
        ani = FuncAnimation(fig, update, frames=len(self.vertice_anim_data) + len(self.anim_data), interval=500, repeat=False)
        plt.show()