from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, RelationSerializer
from .models import User, UserRelations

def test(request):
    return JsonResponse({'ok': 'ok'}, status=200)

class UserProfile(APIView):
    """
    Get information about user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
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

        return Response(data, status=status.HTTP_200_OK)


class MyProfile(APIView):
    """
    Return auth user profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nickname = request.user
        user = User.objects.get_user_profile(nickname)
        data = {
            "login": user.username,
            "followers": user.num_followers,
            "following": user.num_following,
            "isFollow": False,
            "isMyPage": True,
        }

        return Response(data)


class UserLogout(APIView):
    """
    Logout user
    """

    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


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

class UserSignin(APIView):
    """
    Signin user
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if (request.user.is_authenticated):
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class UserRelation(APIView):
    """
    Allow follow and unfollow user
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Вместе с ответом присылать новое количество follwers
        data = {
            "subscriber_id": request.user.id,
            "target_username": request.data.get("username")
        }

        serializer = RelationSerializer(data=data)
        if serializer.is_valid():
            rel = serializer.save()
            if rel:
                return Response({}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Вместе с ответом присылать новое количество follwers
        data = {
            "subscriber_id": request.user.id,
            "target_username": request.data.get("username")
        }

        serializer = RelationSerializer(data=data)
        if serializer.is_valid():
            rel = serializer.delete(request.user.id, request.data.get("username"))
            return Response({}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

