from django.shortcuts import render
from rest_framework.views import APIView
from .models import ItemsModel
from .serializers import ItemsSerializer,RegistrationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse





class DataList(APIView):
    
    def get(self, request, format=None):
        models = ItemsModel.objects.all()
        serializer = ItemsSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DataUpdateDelete(APIView):
   
    def get_object(self, pk):
        try:
            return ItemsModel.objects.get(pk=pk)
        except ItemsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ItemsSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ItemsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductSearchAPIView(generics.ListAPIView):
    queryset = ItemsModel.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    
class RegistrationView(APIView):
    def post(self, request):
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            
        else:
            data = serializer.errors
        return Response(data)
class LoginView(APIView):
    def post(self, request):
        try:
            # Get username and password from request data
            username = request.data.get('username')
            password = request.data.get('password')

            # Check if username and password are provided
            if not username or not password:
                return JsonResponse({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate user
            user = authenticate(username=username, password=password)

            # Check if user is authenticated
            if user is not None:
                # Login user
                login(request, user)
                return JsonResponse({'response': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle any unexpected exceptions
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
        def post(self, request):
            request.user.auth_token.delete()
            return Response(status = status.HTTP_200_OK)
