import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._classificazioni = []
        self._idMapC = {}

    def buildGraph(self, loca):
        self._graph.clear()
        self._classificazioni = DAO.getAllNodes(loca)
        for c in self._classificazioni:
            self._idMapC[c.GeneID] = c

        self._graph.add_nodes_from(self._classificazioni)

        edges = DAO.getAllEdges(loca, self._idMapC)

        for e in edges:
            self._graph.add_edge(e.gen1, e.gen2, weight=e.peso)

    def getTop3Archi(self):
        lista3Top = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=False)

        # DAL PIù PICCOL OAL PIù GRANDE
        return lista3Top[0:]

    def getComponentiConnesse(self):
        components = list(nx.connected_components(self._graph))
        components = [c for c in components if len(c) > 1]
        components = sorted(components, key=len, reverse=True)
        return components

    def cercaSequenza(self):
        self._bestPath = []
        self._bestNumComponents = float("inf")

        nodi = list(self._graph.nodes())
        nodi = [n for n in nodi if n.Essential != "?"]
        nodi = sorted(nodi, key=lambda n: n.GeneID)
        self._ricorsione([], nodi)
        return self._bestPath

    def _ricorsione(self, parziale, nodi):
        if len(parziale) > len(self._bestPath):
            self._bestPath = parziale.copy()
            self._bestNumComponents = self._numComponenti(parziale)

        elif len(parziale) == len(self._bestPath):
            numComp = self._numComponenti(parziale)
            if numComp < self._bestNumComponents:
                self._bestPath = parziale.copy()
                self._bestNumComponents = numComp

        for n in nodi:
            if len(parziale) == 0:
                parziale.append(n)
                self._ricorsione(parziale, nodi)
                parziale.pop()

            else:
                ultimo = parziale[-1]

                if n.GeneID > ultimo.GeneID and n.Essential == parziale[0].Essential:
                    parziale.append(n)
                    self._ricorsione(parziale, nodi)
                    parziale.pop()

    def _numComponenti(self, listaNodi):
        subgraph = self._graph.subgraph(listaNodi)

        return nx.number_connected_components(subgraph)


    def getAllLocalization(self):
        return DAO.getAllLocalizzazione()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)