from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from leaderonomics.permissions import IsOwnerOrReadOnly
from leaderonomics.models import Articles, User
from leaderonomics.serializers import UserSerializer, ArticlesSerializer, AuthenticatedArticlesSerializer


class Logout(APIView):
    queryset = User.objects.all()

    def delete(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

logout = Logout.as_view()


class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        else:
            serializer_class = ArticlesSerializer
        return serializer_class


class ArticlesDetail(generics.RetrieveAPIView):
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        return serializer_class

    queryset = Articles.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

