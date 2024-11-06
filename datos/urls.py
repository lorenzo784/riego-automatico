from django.urls import path
from .views import ObtenerDatos, GuardarDatos, RegistrarAguaAPIView, ResetearAgua, DatosCache

urlpatterns = [
    path('guardar-datos/', GuardarDatos.as_view(), name='guardar_datos'),
    path('', ObtenerDatos.as_view(), name='obtener_datos'),
    path('datos/', DatosCache.as_view(), name='obtener_datos'),
    path('registrar-agua/', RegistrarAguaAPIView.as_view(), name='registrar-agua'),
    path('resetear-agua/', ResetearAgua.as_view(), name='resetear_agua'),
]