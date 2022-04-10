import rest_framework_simplejwt
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_page, cache_control, never_cache
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'put']

    @method_decorator(never_cache)
    def put(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            user.first_name = data.get('first name', user.first_name)
            user.last_name = data.get('last name', user.last_name)
            user.email = data.get('email', user.email)
            user.professor.TableName = data.get('table name', user.professor.TableName)

            if data.get('password'):
                user.set_password(data.get('password'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response(status=400)
    
    @method_decorator(never_cache)
    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'first name': user.first_name,
            'last name': user.last_name,
            'table name': user.professor.TableName
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@never_cache
def login(request):
    data = json.loads(request.body)
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            data={'refresh': str(refresh), 'access': str(refresh.access_token)},
            status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@never_cache
def refresh(request):
    data = json.loads(request.body)
    try:
        refresh = RefreshToken(token=data['refresh'])
    except rest_framework_simplejwt.exceptions.TokenError as e:
        return Response(status=404)
    return Response(
        data={
            'refresh': str(refresh),
            'access': str(refresh.access_token)},
        status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@never_cache
def register(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(username=data.get('username'), password=data.get('password'))
        user.professor.TableName = data.get('table_name', 'Unknown')
        user.save()

        return Response(status=201)
    
    except:
        return Response(status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_users(request):
    users = User.objects.all()
    content = {}
    for u in users:
        content[u.id] = '{}, {}'.format(u.username, u.professor.TableName)
    return Response(data=content, status=200)