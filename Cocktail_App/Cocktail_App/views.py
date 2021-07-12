from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import status

from Cocktail_App.models import Ingredient
from Cocktail_App.models import Recipe
from Cocktail_App.serializers import RecipeSerializer
from Cocktail_App.serializers import IngredientSerializer
from Cocktail_App.permissions import IsOwnerOrReadOnly

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
