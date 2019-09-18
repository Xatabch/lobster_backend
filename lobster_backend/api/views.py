from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserRelations
from .models import User

def test(request):
    return JsonResponse({'ok': 'ok'}, status=200)

class UserProfile(APIView):
    """
    Get information about user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        if(username):
            user = User.objects.get_user_profile(username)
            my_username = request.user
            is_follow = UserRelations.objects.is_follow(my_username, username)
            is_my_page = False

            if (my_username.username == username):
                is_my_page = True

            data = {
                "login": user.username,
                "followers": user.num_followers,
                "following": user.num_following,
                "isFollow": is_follow.count() != 0,
                "isMyPage": is_my_page
            }
        else:
            user = User.objects.get_user_profile(request.user)
            data = {
                "login": user.username,
                "followers": user.num_followers,
                "following": user.num_following,
                "isFollow": False,
                "isMyPage": True,
            }   

        return Response(data, status=status.HTTP_200_OK)

class UserSignup(APIView):
    """
    Signup user
    """
    def post(self, request):
        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            user = serializers.save()
            if user:
                login(request, user)
                return Response({}, status=status.HTTP_201_CREATED)

        # Добавить текст ошибки serializer-а
        return Response({}, status=status.HTTP_403_FORBIDDEN)

