from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .serializers import UserSerializer
from .models import User

# @csrf_exempt
# def test(request):
#     if (request.method == 'OPTIONS'):
#         resp = JsonResponse({}, status=200)
#         resp['Access-Control-Allow-Origin'] = 'http://localhost:8001'
#         resp['Access-Control-Allow-Headers'] = 'Content-Type'
#         resp['Access-Control-Allow-Credentials'] = 'true'
#         resp['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#         return resp;

#     if (request.method == 'POST'):
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         print(body)
#         user = User.objects.create_user(username=body['username'], email=body['email'], password=body['password'])
#         if user:
#             login(request, user)
#             resp = JsonResponse({'post': 'post'}, status=200)
#             resp['Access-Control-Allow-Origin'] = 'http://localhost:8001'
#             resp['Access-Control-Allow-Credentials'] = 'true'
#             return resp;

#         resp = JsonResponse({'post': 'post'}, status=403)
#         return resp;


#     return JsonResponse({}, status=404)

def test(request):
    return JsonResponse({'ok': 'ok'}, status=200)

class UserSignup(APIView):
    """
    Signup user
    """

    def options(self, request):
        return Response({}, status=status.HTTP_200_OK, headers={
            'Access-Control-Allow-Origin': 'http://localhost:8001',
            'Access-Control-Allow-Headers': 'Content-Type, X-CSRFToken',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        })

    def post(self, request):
        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            user = serializers.save()
            if user:
                login(request, user)
                return Response({}, status=status.HTTP_201_CREATED, headers={
                    'Access-Control-Allow-Origin': 'http://localhost:8001',
                    'Access-Control-Allow-Credentials': 'true',
                })

        return Response({"error": "error"}, status=status.HTTP_403_OK, headers={
                    'Access-Control-Allow-Origin': 'http://localhost:8001',
                    'Access-Control-Allow-Credentials': 'true',
                })

