from django.shortcuts import render
from joblib import load
from django.conf import settings
import json 
import os 
model = load("./model/modelo.joblib")
le_marca = load("./model/le_marca.joblib")
le_modelo = load("./model/le_modelo.joblib")
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

def formularioClasificador(request):
    if request.method == "POST":
        # Imprimir el contenido del request.POST para depuración
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.POST)

        # Obtener los datos del formulario
        dinero_disponible = float(request.POST["dinero_disponible"])
        marca = request.POST["marca"]
        modelo = request.POST["modelo"]

        try:
            # Imprimir las clases de le_marca
            pp.pprint(f"Clases disponibles en le_marca: {le_marca.classes_}")

            # Verificar que la marca esté en las clases
            if marca not in le_marca.classes_:
                error_message = f"Marca desconocida: {marca}. Las clases disponibles son: {le_marca.classes_}"
                pp.pprint(error_message)
                return render(request, "resultadoClasificador.html", {"error": error_message})

            # Transformar la marca
            marca_encoded = le_marca.transform([marca])[0]  # Transformar a número

            # Manejar modelo desconocido
            if modelo not in le_modelo.classes_:
                error_message = f"Modelo desconocido: {modelo}. Las clases disponibles son: {le_modelo.classes_}"
                pp.pprint(error_message)
                return render(request, "resultadoClasificador.html", {"error": error_message})

            # Transformar el modelo
            modelo_encoded = le_modelo.transform([modelo])[0]  # Transformar a número

            # Crear un nuevo DataFrame para la predicción
            nuevo_dato = pd.DataFrame([[dinero_disponible, marca_encoded, modelo_encoded]],
                                       columns=['Precio de venta', 'Marca', 'Modelo'])

            # Hacer la predicción
            prediccion_categoria = clasificador.predict(nuevo_dato)
            categoria_solicitante = le_categoria.inverse_transform(prediccion_categoria)[0]

            # Renderizar la respuesta
            return render(request, "resultadoClasificador.html", {"response": categoria_solicitante})

        except ValueError as e:
            # Manejo de error si la transformación falla
            error_message = f"Error al transformar marca o modelo: {e}"
            pp.pprint(error_message)
            return render(request, "resultadoClasificador.html", {"error": error_message})

    return render(request, "resultadoClasificador.html")

