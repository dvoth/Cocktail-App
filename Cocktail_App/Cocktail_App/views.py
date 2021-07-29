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
 
class AvailableRecipesViewset(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # Get all ingredients the user has
        currentUser = self.request.user
        userIngredientIds = UserIngredient.objects.filter(user=currentUser).values_list('ingredient_id', flat=True)

        # For performance, find all the ingredients the user does not have
        inner_queryset = RecipeIngredient.objects.exclude(ingredient_id__in = userIngredientIds)

        # Exclude all recipes where the user does not have the ingredient
        queryset = Recipe.objects.exclude(recipeingredient__in = inner_queryset)

        return queryset