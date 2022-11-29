from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *
from Apps.comercianteExtranjero.models import Licitacion
from Apps.comercianteExtranjero.serializers import LicitacionSerializer
from Apps.productor.models import Oferta
from Apps.productor.serializers import OfertaSerializer
from Apps.productor.models import VentaLocal
from Apps.productor.serializers import VentaLocalSerializer

# Create your views here.
class CrearContratoView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContratoSerializer

class VerContratosView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get (self, request):
        contratos = Contrato.objects.all()
        serializer = ContratoSerializer(contratos, many=True)
        return Response(serializer.data)

class BuscarContratoView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post (self, request,):
        data = self.request.data
        companyName = data['companyName']
        contratos = Contrato.objects.get(companyName=companyName)
        serializer = ContratoSerializer(contratos)
        return Response(serializer.data)
        
class VerLicitacionView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get (self, request):
        solicitud = Licitacion.objects.all()
        serializer = LicitacionSerializer(solicitud, many=True)
        return Response(serializer.data)
        
class VerOfertaView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        oferta = Oferta.objects.all()
        serializer = OfertaSerializer(oferta, many=True)
        return Response(serializer.data)

class VerVentaLocalView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        def get(self, request):
            ventaLocal = VentaLocal.objects.all()
            serializer = VentaLocalSerializer(ventaLocal, many=True)
            return Response(serializer.data)



