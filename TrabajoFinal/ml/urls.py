from django.urls import path
from . import views
app_name = "ml"
urlpatterns = [
    path("" , views.index, name="ml" ),
    path("clasificador" , views.Clasificador, name="ml" ),
    path("modeloPrecioCategoria" , views.regresionPrecioCategoria, name="ml" ),
    path("modeloGananciaCategoria" , views.modeloGananciaCategoria, name="ml" ),
    path("stockCategoria" , views.stockCategoria, name="ml" ),

]