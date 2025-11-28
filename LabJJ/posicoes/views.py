from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from posicoes.serializers import BJJPosSerializer
from posicoes.models import BJJPos
from posicoes.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PosicaoView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_summary="Recupera uma posição específica ou todas",
        responses={200: BJJPosSerializer(many=True), 404: "Não encontrada"}
    )
    def get(self, request, id_arg=None):
        if id_arg:
            try:
                pos = BJJPos.objects.get(id=id_arg)
                return Response(BJJPosSerializer(pos).data)
            except BJJPos.DoesNotExist:
                return Response({"msg": f"Posição {id_arg} não existe"}, status.HTTP_404_NOT_FOUND)

        posicoes = BJJPos.objects.all().order_by("nome_pt")
        return Response(BJJPosSerializer(posicoes, many=True).data)

    @swagger_auto_schema(
        operation_summary="Cria nova posição",
        request_body=BJJPosSerializer,
        responses={201: BJJPosSerializer}
    )
    def post(self, request):
        serializer = BJJPosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Atualiza posição",
        request_body=BJJPosSerializer
    )
    def put(self, request, id_arg):
        try:
            pos = BJJPos.objects.get(id=id_arg)
        except BJJPos.DoesNotExist:
            return Response({"msg": f"Posição {id_arg} não existe"}, status.HTTP_404_NOT_FOUND)

        serializer = BJJPosSerializer(pos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PosicoesView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAuthenticated()]

    @swagger_auto_schema(operation_summary="Lista todas as posições")
    def get(self, request):
        posicoes = BJJPos.objects.all().order_by("nome_pt")
        return Response(BJJPosSerializer(posicoes, many=True).data)

    @swagger_auto_schema(
        operation_summary="Deleta múltiplas posições",
        request_body=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
    )
    def delete(self, request):
        erros = []
        for pos_id in request.data:
            try:
                BJJPos.objects.get(id=pos_id).delete()
            except BJJPos.DoesNotExist:
                erros.append(pos_id)

        if erros:
            return Response({"Erro": f"IDs não encontrados: {erros}"}, status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
