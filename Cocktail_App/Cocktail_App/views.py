from rest_framework import viewsets

from accounts.models import UserIngredient
from Cocktail_App.models import Ingredient
from Cocktail_App.models import Recipe
from Cocktail_App.models import RecipeIngredient
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
 