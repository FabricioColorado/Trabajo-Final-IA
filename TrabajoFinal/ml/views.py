from django.shortcuts import render
from joblib import load
from django.conf import settings
import json 
import os 
# model = load("./model/iris_model.joblib")
def index(request):
    with open('data/data.json') as f:
        data = json.load(f)
    items = [
        {
            "id": index + 1,  # Generamos un ID único comenzando desde 1
            "CodInterno": item["Cod. Interno"],
            "Nombre": item["Nombre"],
            "Categoria": item["Categoria"],
            "PrecioVenta": item["Precio de venta"],
            "GananciaTotal": item["Ganancia Total"],
            "Marca": item["Marca"],
            "Modelo": item["Modelo"]
        }
        for index, item in enumerate(data)  
    ]
    return render(request, 'index.html', {'data': items})

def Clasificador(request):
    return render(request, 'clasificador.html')

def regresionPrecioCategoria(request):
    return render(request, 'modeloPrecioCategoria.html')

def modeloGananciaCategoria(request):
    return render(request, 'modeloGananciaCategoria.html')


def stockCategoria(request):
    return render(request, 'stockCategoria.html')
# Create your views here.
