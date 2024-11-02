from django.urls import path
from . import views
app_name = "ml"

urlpatterns = [
    path("" , views.index, name="ml" ),
    path("clasificador" , views.Clasificador, name="clasificador" ),
    path("modeloPrecioCategoria" , views.regresionPrecioCategoria, name="modelo_precio_categoria" ),
    path("modeloGananciaCategoria" , views.modeloGananciaCategoria, name="modelo_ganancia_categoria" ),
    path("stockCategoria" , views.stockCategoria, name="stock_categoria" ),
    path("clasificarData", views.formularioClasificador, name="clasificar_data")

]