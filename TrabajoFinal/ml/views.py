from django.shortcuts import render
from joblib import load
model = load("./model/iris_model.joblib")
def index(request):
    return render(request, 'index.html')

def Clasificador(request):
    return render(request, 'clasificador.html')

def regresionPrecioCategoria(request):
    return render(request, 'modeloPrecioCategoria.html')

def modeloGananciaCategoria(request):
    return render(request, 'modeloGananciaCategoria.html')


def stockCategoria(request):
    return render(request, 'stockCategoria.html')
# Create your views here.
