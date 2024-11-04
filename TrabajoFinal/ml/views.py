from django.shortcuts import render
from joblib import load
from django.conf import settings
import json 
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  

def index(request):
    with open('data/data.json') as f:
        data = json.load(f)
    items = [
        {
            "id": index + 1, 
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


model = load("./model/modelo.joblib")
le_marca = load("./model/le_marca.joblib")
le_y = load("./model/le_y.joblib")
def formularioClasificador(request):
    with open('data/data.json') as f:
        data = json.load(f)
    data = pd.DataFrame(data)  
    if request.method == "POST":
        try:
            dinero_disponible = float(request.POST["dinero_disponible"])
            marca = request.POST["marca"]

            nuevo_dato = pd.DataFrame([[dinero_disponible, marca]], columns=['Precio de venta', 'Marca'])
            nuevo_dato['Marca'] = le_marca.transform(nuevo_dato['Marca'])

            prediccion_categoria = model.predict(nuevo_dato)
            categoria_solicitante = le_y.inverse_transform(prediccion_categoria)[0]

            plt.figure(figsize=(15, 10))
            for categoria in le_y.classes_:
                categoria_data = data[data['Categoria'] == categoria]
                if not categoria_data.empty:
                    plt.scatter([categoria] * len(categoria_data), categoria_data['Precio de venta'],
                                marker="*", s=150, label=categoria, alpha=0.6)

            solicitante_categoria_index = le_y.transform([categoria_solicitante])[0]
            plt.scatter(solicitante_categoria_index, dinero_disponible, marker="P", s=250, color="green", label="Solicitante")

            plt.ylabel("Precio de venta (S/)")
            plt.xlabel("Categoría")
            plt.xticks(ticks=np.arange(len(le_y.classes_)), labels=le_y.classes_, rotation=45, ha='right')
            plt.title("Distribución de Precios por Categoría")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            image_path = os.path.join("ml", "static", "images", "grafico.png")
            
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            plt.savefig(image_path)
            plt.close()  

            return render(request, "resultadoClasificador.html", {
                "response": categoria_solicitante,
                "grafico": image_path 
            })

        except ValueError as e:
            return render(request, "resultadoClasificador.html", {"error": "Error en los datos de entrada."})
        except Exception as e:
            return render(request, "resultadoClasificador.html", {"error": "Ocurrió un error inesperado: " + str(e)})

    return render(request, "resultadoClasificador.html")

