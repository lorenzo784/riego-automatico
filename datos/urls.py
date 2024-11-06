from django.urls import path
from .views import ObtenerDatos, GuardarDatos, RegistrarAguaAPIView, ResetearAgua, DatosCache, bomba, ControlBombaAPIView

urlpatterns = [
    path('guardar-datos/', GuardarDatos.as_view(), name='guardar_datos'),
    path('', ObtenerDatos.as_view(), name='inicio'),
    path('datos/', DatosCache.as_view(), name='obtener_datos'),
    path('registrar-agua/', RegistrarAguaAPIView.as_view(), name='registrar-agua'),
    path('resetear-agua/', ResetearAgua.as_view(), name='resetear_agua'),
    path('estado_bomba/', bomba.as_view(), name='estado_bomba'),
    path('control-bomba/', ControlBombaAPIView.as_view(), name='control_bomba'),
]