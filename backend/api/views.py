from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from users.models import User
from recipes.models import Ingredient, Tag, Recipe

from .serializers import UserSerializer, IngredientSerializer, TagSerializer, RecipeSerializer


from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import filters, serializers, status, views
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer

class UserViewSet(BaseUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    search_fields = ['author__id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['GET'],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        """
        Возвращает короткую ссылку на рецепт.
        """

        recipe = self.get_object()
        full_short_link = request.build_absolute_uri(
            reverse(
                'recipe-shortlink',
                kwargs={'short_link': recipe.short_link},
            )
        )
        return Response(
            {'short-link': full_short_link},
            status=status.HTTP_200_OK,
        )