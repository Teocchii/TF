import csv
import heapq

# Librerías para la interfaz
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Librerías para el grafo
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.vertices = {}
    
    def agregar_vertice(self, vertice):
        self.vertices[vertice] = {}

    def agregar_arista(self, inicio, fin, peso):
        self.vertices[inicio][fin] = peso

    def obtener_peso(self, inicio, fin):
        return self.vertices[inicio][fin]
    
    def obtener_vertices(self):
        return list(self.vertices.keys())

    def obtener_fronteras(self, vertice):
        return list(self.vertices[vertice].keys())
        
def cargar_datos(archivo):
    g = Grafo()

    with open(archivo, 'r') as archivo_csv:
        dictReader = csv.DictReader(archivo_csv)
        for fila in dictReader:
            departamento = fila['DEPARTAMENTO']
            codigo_via = fila['CODIGO_VIA']
            destino = fila['DESTINO']
            riesgo = int(fila['RIESGO'])

            if departamento not in g.obtener_vertices():
                g.agregar_vertice(departamento)
        
            if destino not in g.obtener_vertices():
                g.agregar_vertice(destino)

            g.agregar_arista(departamento, destino, riesgo)
            g.agregar_arista(destino, departamento, riesgo)

    return g

def dijkstra(grafo, inicio, fin, recorridoMinimo, evitar):
    recorridos = {vertice: float('inf') for vertice in grafo.obtener_vertices()}
    recorridos[inicio] = 0

    heap = [(0, inicio)]
    padres = {}

    while heap:
        recorridoActual, verticeActual = heapq.heappop(heap)
        if recorridoActual > recorridos[verticeActual]:
            continue

        if verticeActual == fin and len(set(padres.values())) >= recorridoMinimo:
            break

        for frontera in grafo.obtener_fronteras(verticeActual):
            if frontera == evitar:
                continue
            pesoArista = grafo.obtener_peso(verticeActual, frontera)
            recorrido = pesoArista + recorridoActual

            if recorrido < recorridos[frontera]:
                recorridos[frontera] = recorrido
                heapq.heappush(heap, (recorrido, frontera))
                padres[frontera] = verticeActual

    if fin not in padres or len(set(padres.values())) < recorridoMinimo:
        return None

    ruta = []
    nodo_actual = fin 

    while nodo_actual != inicio:
        ruta.append(nodo_actual)
        nodo_actual = padres[nodo_actual]

    ruta.append(inicio)
    ruta.reverse()
    return ruta

def ruta_con_nodo_intermedio(grafo, inicio, intermedio, fin, recorridoMinimo, evitar):
    ruta_1 = dijkstra(grafo, inicio, intermedio, recorridoMinimo, evitar)
    if not ruta_1:
        return None

    ruta_2 = dijkstra(grafo, intermedio, fin, recorridoMinimo, evitar)
    if not ruta_2:
        return None

    return ruta_1[:-1] + ruta_2

def mostrar_grafo(grafo):
    g = nx.Graph()

    for vertice in grafo.obtener_vertices():
        g.add_node(vertice)

    for inicio in grafo.obtener_vertices():
        for fin in grafo.obtener_fronteras(inicio):
            riesgo = grafo.obtener_peso(inicio, fin)
            g.add_edge(inicio, fin, weight=riesgo)
        
    pos = nx.spring_layout(g)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx(g, with_labels=True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()

class FormularioRuta(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Formulario de Ruta")
        self.geometry("300x300")
        
        self.origen = None
        self.destino = None
        self.intermedio = None
        self.evitar = None

        self.crear_formulario()

    def crear_formulario(self):
        ttk.Label(self, text="Origen:").pack(pady=5)
        self.entry_origen = ttk.Entry(self)
        self.entry_origen.pack(pady=5)

        ttk.Label(self, text="Destino:").pack(pady=5)
        self.entry_destino = ttk.Entry(self)
        self.entry_destino.pack(pady=5)

        ttk.Label(self, text="Nodo Intermedio (Opcional):").pack(pady=5)
        self.entry_intermedio = ttk.Entry(self)
        self.entry_intermedio.pack(pady=5)

        ttk.Label(self, text="Nodo a Evitar (Opcional):").pack(pady=5)
        self.entry_evitar = ttk.Entry(self)
        self.entry_evitar.pack(pady=5)

        boton_aceptar = ttk.Button(self, text="Aceptar", command=self.aceptar)
        boton_aceptar.pack(pady=20)

    def aceptar(self):
        self.origen = self.entry_origen.get()
        self.destino = self.entry_destino.get()
        self.intermedio = self.entry_intermedio.get()
        self.evitar = self.entry_evitar.get()
        self.destroy()

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WarnedRoute")
        self.opciones()
        self.fondo()

    def opciones(self):
        frameOpciones = tk.Frame(self.ventana)
        frameOpciones.pack()

        boton_mostrar = tk.Button(frameOpciones, text="Mostrar el grafo", command=self.mostrar_grafo_interfaz)
        boton_mostrar.pack(padx=20, pady=20)
        
        boton_integrantes = tk.Button(frameOpciones, text="Integrantes Grupo:", command=self.mostrar_integrantes)
        boton_integrantes.pack(padx=20, pady=20)

        boton_ruta_segura = tk.Button(frameOpciones, text="Ruta segura", command=self.ruta_segura)
        boton_ruta_segura.pack(padx=20, pady=20)

    def mostrar_grafo_interfaz(self):
        grafo = cargar_datos('dataset.csv')
        mostrar_grafo(grafo)
    
    def mostrar_integrantes(self):
        messagebox.showinfo("Integrantes", "Daniel Del Castillo\nGustavo Poma\nDiego Melendez")
    
    def fondo(self):
        logo = tk.PhotoImage(file="fondo.png")
        label = tk.Label(self.ventana, image=logo)
        label.image = logo
        label.pack()

    def ruta_segura(self):
        formulario = FormularioRuta(self.ventana)
        self.ventana.wait_window(formulario)

        origen = formulario.origen
        destino = formulario.destino
        intermedio = formulario.intermedio
        evitar = formulario.evitar
        recorridoMinimo = 3

        if origen and destino:
            grafo = cargar_datos('dataset.csv')
            if intermedio:
                ruta_segura = ruta_con_nodo_intermedio(grafo, origen, intermedio, destino, recorridoMinimo, evitar)
            else:
                ruta_segura = dijkstra(grafo, origen, destino, recorridoMinimo, evitar)

            if ruta_segura:
                messagebox.showinfo("Ruta segura", f"La ruta segura es: {' -> '.join(ruta_segura)}")
            else:
                messagebox.showwarning("Ruta muy peligrosa", "No se encontró una ruta estadísticamente segura para llegar a su destino")
        else:
            messagebox.showwarning("Error", "No se ingresaron los datos correctamente")

    def mostrar(self):
        self.ventana.mainloop()

def main():
    ventana = Interfaz()
    ventana.mostrar()

if __name__ == '__main__':
    main()
