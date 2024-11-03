from django.urls import path
from .views import ObtenerDatos, GuardarDatos

urlpatterns = [
    path('guardar-datos/', GuardarDatos.as_view(), name='guardar_datos'),  # URL para guardar datos
    path('obtener-datos/', ObtenerDatos.as_view(), name='obtener_datos'),  # URL para obtener datos
]