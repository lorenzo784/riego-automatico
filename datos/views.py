from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import render

class GuardarDatos(APIView):
    def post(self, request):
        # Obtener los datos de la solicitud POST
        datos_sensor = {
            "temperatura": request.data.get('temperatura'),
            "humedad_ambiente": request.data.get('humedad_ambiente'),
            "humedad_suelo": request.data.get('humedad_suelo'),
            "proximo_riego": request.data.get('proximo_riego'),
            "estado_sistema": request.data.get('estado_sistema'),
        }

        # Guardar en caché por 1 hora (3600 segundos)
        cache.set('datos_sensor', datos_sensor, timeout=3600)

        return Response({"message": "Datos guardados temporalmente"}, status=status.HTTP_201_CREATED)


class ObtenerDatos(APIView):
    def get(self, request):
        # Recuperar los datos de la caché
        datos_sensor = cache.get('datos_sensor')

        if datos_sensor:
            # Renderizar la plantilla HTML 'mostrar_datos.html' con los datos
            return render(request, 'datos/mostrar_datos.html', datos_sensor)
        else:
            # Si no hay datos en la caché, establecer valores por defecto
            datos_default = {
                'temperatura': 'NA',
                'humedad_ambiente': 'NA',
                'humedad_suelo': 'NA',
                'proximo_riego': 'NA',
                'estado_sistema': 'NA'
            }
            # Renderizar la plantilla HTML 'mostrar_datos.html' con valores por defecto
            return render(request, 'datos/mostrar_datos.html', datos_default)