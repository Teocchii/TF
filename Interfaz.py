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
        self.vertices[vertice]=[]

    def agregar_arista(self, inicio, fin, peso):
        self.vertices[inicio][fin]=peso

    def obtener_peso(self, inicio, fin):
        return self.vertices[inicio][fin]
    
    #Esta funcion obtener_vertices hace que los nombres de los vertices sean una lista
    def obtener_vertices(self):
        return list(self.vertices.keys())

    def obtener_fronteras(self,vertice):
        return list(self.vertices[vertice].keys())
        
        