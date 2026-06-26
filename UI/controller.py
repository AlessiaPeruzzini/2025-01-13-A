import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph(self._view.dd_localization.value)
        Nnodes, Nedges = self._model.getGraphDetails()

        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato: "))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {Nedges}"))

        top5 = self._model.getTop3Archi()

        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))

        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} : peso {arco[2]["weight"]}"))

        self._view.update_page()

    def analyze_graph(self, e):
        components = self._model.getComponentiConnesse()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Le componenti connesse sono:")
        )

        for c in components:
            nodi = sorted(list(c), key=lambda n: n.GeneID)

            stringa_nodi = ", ".join([str(n.GeneID) for n in nodi])

            self._view.txt_result.controls.append(
                ft.Text(f"{stringa_nodi}, | dimensione componente = {len(c)}")
            )

        self._view.update_page()

    def handle_path(self,e):
        soluzione = self._model.cercaSequenza()

        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(
            ft.Text("Sequenza trovata:")
        )

        stringa = ", ".join([str(n.GeneID) for n in soluzione])

        self._view.txt_result.controls.append(
            ft.Text(stringa)
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Lunghezza sequenza = {len(soluzione)}")
        )

        self._view.update_page()


    def filDDLoca(self):
        loca = self._model.getAllLocalization()
        locaDD = list(map(lambda x: ft.dropdown.Option(data=x, key=x.Localization, on_click = self.handleDDloca), loca))

        self._view.dd_localization.options = locaDD

        self._view.update_page()

    def handleDDloca(self, e):
        self._loca = e.control.data

