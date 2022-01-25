from drf_writable_nested import serializers
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer

from .models import CustomUser, Follow
from .serializers import (
    CustomUserSerializer, FollowSerializer,
    FollowUserSerializer, UserRegistrationSerializer)
from .pagintations import CustomPagination
from .permissions import OwnOrReadOrRegister


User = CustomUser()


class set_pass(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SetPasswordSerializer
    permission_class = (permissions.IsAuthenticated, )
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(serializer.data)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
    permission_classes = (OwnOrReadOrRegister, )
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return UserRegistrationSerializer

    @action(
        detail=False,
        methods=['GET', ],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me')
    def me(self, request):
        user = self.request.user
        instance = CustomUser.objects.get(username=user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = self.get_object()
        user = self.request.user
        if request.method == 'POST':
            if Follow.objects.filter(author=author, user=user).exists():
                data = {'detail': "Уже подписаны!"}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            elif author == user:
                data = {'detail': 'Нелья подписываться на самого себя!'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['GET'],
        permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowUserSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
