from django.shortcuts import render
from posicoes.serializers import BJJPosSerializer
from posicoes.models import BJJPos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class PosicoesView(APIView):
    def get(self, req):
        queryset = BJJPos.objects.all().order_by("nome_pt")
        serializer = BJJPosSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, req):
        serializer = BJJPosSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
