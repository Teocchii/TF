#Librerías para generar grafo a partir del dataset
import csv
import heapq

#librerías para la interfaz
import tkinter as tk
from tkinter import messagebox, Menu


#Librerias para el grafo
import networkx as nx
import matplotlib.pyplot as plt



class grafo:
    def __init__(self):
        self.vertices={}
    
    def agregar_vertice(self, vertice):
        
        self.vertices[vertice]={}

    def agregar_arista(self, inicio, fin, peso):
        self.vertices[inicio][fin] = peso

    def obtener_peso(self, inicio, fin):
        return self.vertices[inicio][fin]
    
    #Esta funcion obtener_vertices hace que los nombres de los vertices sean una lista
    def obtener_vertices(self):
        return list(self.vertices.keys())

    def obtener_fronteras(self,vertice):
        return list(self.vertices[vertice].keys())
        
def cargar_datos(archivo):
    g=grafo()

    with open(archivo,'r')as archivo_csv:
        dictReader=csv.DictReader(archivo_csv)
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

def dijkstra(grafo,inicio,fin,recorridoMinimo):
    recorridos={vertice:float('inf')for vertice in grafo.obtener_vertices()}
    recorridos[inicio]=0

    heap=[(0,inicio)]
    padres={}

    while heap:
        recorridoActual, verticeActual=heapq.heappop(heap)
        if recorridoActual>recorridos[verticeActual]:
         continue

        #Excepcion
        if verticeActual== fin and len(set(padres.values()))>=recorridoMinimo:
            break

        for frontera in grafo.obtener_fronteras(verticeActual):
           pesoArista= grafo.obtener_peso(verticeActual,frontera)
           recorrido=pesoArista+recorridoActual

           if recorrido<recorridos[frontera]:
               recorridos[frontera]=recorrido
               heapq.heappush(heap,(recorrido,frontera))
               padres[frontera]=verticeActual

    if fin not in padres or len(set(padres.values()))<recorridoMinimo:
        return None
    
    #Recorrido usado
    ruta=[]
    nodo_actual=fin 

    while nodo_actual != inicio:
        ruta.append(nodo_actual)
        nodo_actual=padres[nodo_actual]

    ruta.append(inicio)
    ruta.reverse()
    return ruta

def mostrar_grafo(grafo):
    g=nx.Graph()

    for vertice in grafo.obtener_vertices():
        g.add_node(vertice)

    for inicio in grafo.obtener_vertices():
        for fin in grafo.obtener_fronteras(inicio):
            riesgo=grafo.obtener_peso(inicio,fin)
            g.add_edge(inicio,fin,weight=riesgo)
        
    pos=nx.spring_layout(g)
    labels=nx.get_edge_attributes(g,'weight')
    nx.draw_networkx(g,with_labels=True)
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
    plt.show()




class Interfaz:
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("WarnedRoute")
        self.opciones()

    def opciones(self):
        frameOpciones=tk.Frame(self.ventana)
        frameOpciones.pack()

        boton_mostrar=tk.Button(frameOpciones,text="Mostrar el grafo",command=self.mostrar_grafo_interfaz)
        boton_mostrar.pack(pady=20)
        
        boton_integrantes=tk.Button(frameOpciones,text="Integrantes Grupo:",command=self.mostrar_integrantes)
        boton_integrantes.pack(pady=20)

        

   


    def mostrar_grafo_interfaz(self):
        grafo=cargar_datos('dataset.csv')
        mostrar_grafo(grafo)
    
    def mostrar_integrantes(self):
        messagebox.showinfo("Integrantes","Daniel Del Castillo\nGustavo Poma\nDiego Melendez")

    def ruta_segura(self):
        origen=self.obtenerOrigen()
        destino=self.obtenerDestino()
        recorridoMinimo=2

        if origen and destino:
             grafo=cargar_datos('dataset.csv')
             ruta_segura=dijkstra(grafo,origen,destino,recorridoMinimo)

             if ruta_segura:
                 messagebox.showinfo("Ruta segura","La ruta segura es: ",f"->".join(ruta_segura))
             else:
                 messagebox.showwarning("Ruta muy peligrosa,No se encontró una ruta estadisticamente segura para llegar a su destino")
        else:
            messagebox.showwarning("Error","No se ingresaron los datos correctamente")


    def obtenerOrigen(self):
        return tk.simpledialog.askstring("Origen","Ingrese el departamento de inicio")
    
    def obtenerDestino(self):
        return tk.simpledialog.askstring("Destino","Ingrese el departamento de destino")
    








    def mostrar(self):
        self.ventana.mainloop()

def main():
    ventana=Interfaz()
    ventana.mostrar()

    
if __name__ == '__main__':
    main()

    