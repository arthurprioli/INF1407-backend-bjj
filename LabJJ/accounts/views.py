from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, status
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer

# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    '''
    View para gerenciamento de tokens de autenticação
    '''
    @swagger_auto_schema(
        operation_summary='obter o token de autenticação',
        operation_description='Retorna o token em caso de sucesso na autenticação ou HTTP 401',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password', ],
        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_summary='Obtém o username do usuário',
        operation_description="Retorna o username do usuário ou apenas visitante se o usuário nsecurity=[{'Token':[]}]",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                default='token ',
                ),
        ],
        responses={
            200: openapi.Response(
                description='Nome do usuário',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'username': openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        }
    )
    def get(self, request):
        '''
        Parâmetros: o token de acesso
        Retorna: o username ou 'visitante'
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response(
            {'username': user.username},
            status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response({'username': 'visitante'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Realiza logout do usuário, apagando o seu token',
        operation_summary='Realiza logout',
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING, default='token ',
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
            ),
        ],
        request_body=None,
        responses={
            status.HTTP_200_OK: 'User logged out',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated',
            status.HTTP_403_FORBIDDEN: 'User not authorized to logout',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Erro no servidor',
        },
    )
    def delete(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            token_obj = Token.objects.get(key=token)
        except (Token.DoesNotExist, IndexError):
            return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST)
        user = token_obj.user
        if user.is_authenticated:
            request.user = user
            logout(request)
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'msg': 'Logout bem-sucedido.'},status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Usuário não autenticado.'},status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_description='Troca a senha do usuário, atualiza o token em caso de sucesso',
        operation_summary='Troca a senha do usuário',
        manual_parameters=[
            openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
            default='token ',
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['old_password', 'new_password1', 'new_password2'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Senha alterada com sucesso.",
                examples={ "application/json": { "message": "Senha alterada com sucesso." } }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na solicitação.",
                examples={ "application/json": { "old_password": ["Senha atual incorreta."] } }
            ),
        }
    )
    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        oldPassword = request.data.get('old_password')
        newPassword = request.data.get('new_password1')
        confirmPassword = request.data.get('new_password2')
        if newPassword != confirmPassword:
            return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        # Verificar se a senha atual está correta
        if user.check_password(oldPassword):
            # Alterar a senha e atualizar o token
            user.set_password(newPassword)
            user.save()

            try:
                token = Token.objects.get(user=user)
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                pass
            return Response({'token': token.key, "message": "Senha alterada com sucesso."},status=status.HTTP_200_OK)
        else:
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)

class Registro(generics.CreateAPIView):
    '''
    Permite criar um usuário
    '''

    permission_classes = [AllowAny]  # Qualquer um pode se registrar
    authentication_classes = []      # Não precisa estar autenticado

    @swagger_auto_schema(
        operation_summary="Registrar novo usuário",
        operation_description="Cria um novo usuário e retorna o token de autenticação",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'password_confirm'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Nome de usuário único',
                    example='arthur411'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description='Senha do usuário',
                    example='senha_forte411'
                ),
                'password_confirm': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description='Confirmação da senha',
                    example='senha_forte411'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='Email opcional',
                    example='arthur@email.com'
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Usuário criado com sucesso",
                examples={
                    "application/json": {
                        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
                        "user": {
                            "id": 42,
                            "username": "arthur411",
                            "email": "arthur@email.com"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Erro de validação",
                examples={
                    "application/json": {
                        "username": ["A user with that username already exists."],
                        "password_confirm": ["As senhas não coincidem."],
                    }
                }
            )
        }
    )
    def post(self, req, *args, **kwargs):
        username = req.data.get("username")
        password = req.data.get("password")
        password_confirm = req.data.get("password_confirm")

        email = req.data.get("email", "")

        if not username or not password:
            return Response(
                {"error": "Usuário e senha são obrigatórios"},
                status = status.HTTP_400_BAD_REQUEST
            )

        if password != password_confirm:
            return Response(
                {"password_confirm": ["As senhas não coincidem."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"username": ["Este nome de usuário já existe!"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.save()

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'estudante'}
            )

            if User.objects.count() == 1:
                profile.role = 'admin'
                profile.save()
                print("ADMIN CRIADO!")

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email or None,
                    'role': user.userprofile.role
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": "Erro ao criar usuário", "detail":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class Logged(APIView):
    @swagger_auto_schema(
        operation_description='Envia Todas as informações de Login do usuário a partir do token',
        operation_summary='Envia informações do usuário logado',
        manual_parameters=[
            openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
            default='token ',
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Informações do usuário",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na solicitação.",
            ),
        }
    )
    def get(self, req):
        authentication_classes = [TokenAuthentication]
        token = req.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        profile = UserProfile.objects.get(user=user)
        return Response(UserProfileSerializer(profile, many=False).data)
