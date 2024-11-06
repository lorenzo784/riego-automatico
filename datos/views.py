from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import render
from .models import RegistroRiego
from django.db import models
import json

class GuardarDatos(APIView):
    def post(self, request):
        datos_sensor = {
            "temperatura": request.data.get('temperatura'),
            "humedad_ambiente": request.data.get('humedad_ambiente'),
            "humedad_suelo": request.data.get('humedad_suelo'),
            "proximo_riego": request.data.get('proximo_riego'),
            "estado_sistema": request.data.get('estado_sistema'),
            "estado_bomba": request.data.get('estado_bomba'),
            "nivel_tanque_agua": request.data.get('nivel_tanque_agua'),
        }

        cache.set('datos_sensor', datos_sensor, timeout=300)

        return Response({"message": "Datos guardados temporalmente"}, status=status.HTTP_201_CREATED)

class ObtenerDatos(APIView):
    def get(self, request):
        datos_sensor = cache.get('datos_sensor')

        total_agua_utilizada = RegistroRiego.objects.aggregate(total=models.Sum('cantidad_agua'))['total'] or 0

        if datos_sensor:
            datos_sensor['total_agua_utilizada'] = total_agua_utilizada
            return render(request, 'datos/mostrar_datos.html', datos_sensor)
        else:
            datos_default = {
                'temperatura': 'NA',
                'humedad_ambiente': 'NA',
                'humedad_suelo': 'NA',
                'proximo_riego': 'NA',
                'estado_sistema': 'NA',
                'estado_bomba': 'NA',
                'nivel_tanque_agua': 'NA',
                'total_agua_utilizada': total_agua_utilizada
            }
            return render(request, 'datos/mostrar_datos.html', datos_default)

class DatosCache(APIView):
    def get(self, request):
        datos_sensor = cache.get('datos_sensor')

        total_agua_utilizada = RegistroRiego.objects.aggregate(total=models.Sum('cantidad_agua'))['total'] or 0

        if datos_sensor:
            datos_sensor['total_agua_utilizada'] = total_agua_utilizada
            return Response(datos_sensor)
        else:
            datos_default = {
                'temperatura': 'NA',
                'humedad_ambiente': 'NA',
                'humedad_suelo': 'NA',
                'proximo_riego': 'NA',
                'estado_sistema': 'NA',
                'estado_bomba': 'NA',
                'nivel_tanque_agua': 'NA',
                'total_agua_utilizada': total_agua_utilizada
            }
            return Response(datos_default)


class RegistrarAguaAPIView(APIView):
    def post(self, request):
        cantidad_agua = request.data.get('cantidad_agua')

        if cantidad_agua is not None:
            try:
                cantidad_agua = float(cantidad_agua)    
                if cantidad_agua > 0:
                    nuevo_riego = RegistroRiego(cantidad_agua=cantidad_agua)
                    nuevo_riego.save()

                    return Response({"message": "Cantidad de agua registrada correctamente"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "La cantidad de agua debe ser mayor a 0"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "La cantidad de agua debe ser un número válido"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Falta el dato de cantidad de agua"}, status=status.HTTP_400_BAD_REQUEST)


class ResetearAgua(APIView):
    def post(self, request):
        RegistroRiego.objects.all().delete()
        return Response({"message": "El agua se ha restablecido correctamente."}, status=200)
    

class bomba(APIView):
    def get(self, request):
        return render(request, 'datos/estado_bomba.html')



class ControlBombaAPIView(APIView):

    def get(self, request):
        estado_bomba = cache.get('estado_bomba')

        if estado_bomba is None:
            estado_bomba = False
            cache.set('estado_bomba', estado_bomba, timeout=60*10) 

        return Response({"estado_bomba": estado_bomba}, status=status.HTTP_200_OK)

    def post(self, request):
        estado_bomba = request.data.get('estado_bomba')

        if estado_bomba is None:
            return Response({"error": "El valor de 'estado_bomba' es necesario."}, status=status.HTTP_400_BAD_REQUEST)

        if estado_bomba == 'true':
            cache.set('estado_bomba', True, timeout=60*10) 
            return Response({"estado_bomba": True}, status=status.HTTP_200_OK)
        elif estado_bomba == 'false':
            cache.set('estado_bomba', False, timeout=60*10)
            return Response({"estado_bomba": False}, status=status.HTTP_200_OK)

        return Response({"error": "El valor de 'estado_bomba' debe ser 'true' o 'false'"}, status=status.HTTP_400_BAD_REQUEST)
