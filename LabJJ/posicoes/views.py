from django.shortcuts import render
from posicoes.serializers import BJJPosSerializer
from posicoes.models import BJJPos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PosicaoView(APIView):

    @swagger_auto_schema(
        operation_summary="Recupera uma posição específica ou todas as posições",
        operation_description="Se a URL incluir um ID, retorna a posição correspondente; caso contrário, retorna todas as posições.",
        responses={
            200: openapi.Response("Sucesso", BJJPosSerializer(many=True)),
            404: "Posição não encontrada",
        },
    )
    def get(self, req, id_arg=None):
        """
        Recupera uma posição de BJJ por ID ou lista todas as posições.

        :param req: Objeto Request do DRF.
        :param id_arg: ID da posição a ser recuperada (opcional, padrão: None).
        :return: Response com a posição única ou a lista de posições.
        :rtype: rest_framework.response.Response
        """
        if id_arg is not None:
            try:
                queryset = BJJPos.objects.get(id=id_arg)
                serializer = BJJPosSerializer(queryset)
                return Response(serializer.data)
            except BJJPos.DoesNotExist:
                return Response(
                    {"msg": f"Posição com id #{id_arg} não existe"},
                    status.HTTP_404_NOT_FOUND,
                )
        queryset = BJJPos.objects.all().order_by("nome_pt")
        serializer = BJJPosSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Cria uma nova posição de jiu-jitsu",
        operation_description="Adiciona uma nova posição ao banco de dados.",
        request_body=BJJPosSerializer,
        responses={
            201: openapi.Response("Criado com sucesso", BJJPosSerializer),
            400: "Dados inválidos",
        },
    )
    def post(self, req):
        """
        Cria uma nova posição de BJJ.

        Os dados da posição devem ser passados no corpo da requisição.

        :param req: Objeto Request do DRF contendo os dados da posição.
        :return: Response com a posição criada e status 201, ou erros de validação e status 400.
        :rtype: rest_framework.response.Response
        """
        serializer = BJJPosSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Atualiza uma posição existente",
        operation_description="Atualiza completamente os dados de uma posição com o ID de caminho fornecido.",
        request_body=BJJPosSerializer,
        responses={
            200: openapi.Response("Atualizado com sucesso", BJJPosSerializer),
            400: "Dados inválidos",
            404: "Posição não encontrada",
        },
    )
    def put(self, req, id_arg):
        """
        Atualiza completamente uma posição de BJJ existente.

        :param req: Objeto Request do DRF contendo os novos dados da posição.
        :param id_arg: ID da posição a ser atualizada.
        :return: Response com os dados atualizados e status 200, ou erros de validação/posição não encontrada.
        :rtype: rest_framework.response.Response
        """
        try:
            posicao = BJJPos.objects.get(id=id_arg)
        except BJJPos.DoesNotExist:
            return Response(
                {"msg": f"Posição com id #{id_arg} não existe"},
                status.HTTP_404_NOT_FOUND,
            )

        serializer = BJJPosSerializer(posicao, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# Create your views here.
class PosicoesView(APIView):
    @swagger_auto_schema(
        operation_summary="Lista todas as posições de jiu-jitsu",
        operation_description="Obtem informações sobre todas as posições",
        request_body=None,
        responses={200: BJJPosSerializer(many=True)},
    )
    def get(self, req):
        """
        Lista todas as posições de BJJ ordenadas por nome em português.

        Este método é tipicamente mapeado para a rota base (e.g., /posicoes/).

        :param req: Objeto Request do DRF.
        :return: Response com a lista de todas as posições e status 200.
        :rtype: rest_framework.response.Response
        """
        posicoes = BJJPos.objects.all().order_by("nome_pt")
        serializer = BJJPosSerializer(posicoes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Deleta múltiplas posições",
        operation_description="Deleta posições com base em uma lista de IDs fornecida no corpo da requisição.",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description="Lista de IDs das posições a serem deletadas. Ex: [1, 5, 8]",
        ),
        responses={
            204: "Deletado com sucesso (sem conteúdo)",
            404: "Um ou mais IDs não foram encontrados",
        },
    )
    def delete(self, req):
        """
        Deleta múltiplas posições de BJJ.

        Espera-se uma lista de IDs no corpo da requisição (JSON array).
        Se algum ID não for encontrado, retorna 404, listando os IDs problemáticos.

        :param req: Objeto Request do DRF contendo a lista de IDs a serem deletados.
        :return: Response vazia e status 204 se sucesso, ou status 404 se algum item não for encontrado.
        :rtype: rest_framework.response.Response
        """
        id_erro = ""
        erro = False
        for id in req.data:
            try:
                posicao = BJJPos.objects.get(id=id)
                posicao.delete()
            except BJJPos.DoesNotExist:
                id_erro += str(id) + ", "
                erro = True

        if erro:
            id_erro = id_erro.strip().rstrip(',')
            return Response(
                {"Erro": f"item(s) [{id_erro}] não encontrado(s)"}, status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)  