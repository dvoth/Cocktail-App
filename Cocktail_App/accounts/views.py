from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from Cocktail_App.models import Ingredient
from Cocktail_App.models import RecipeIngredient
from Cocktail_App.models import Recipe
from accounts.models import UserIngredient
from accounts.models import User
from accounts.serializers import IngredientSerializer
from Cocktail_App.serializers import RecipeSerializer
from accounts.serializers import UserSerializer
from accounts.serializers import UserIngredientSerializer
from knox.auth import TokenAuthentication

# Create your views here.
class UserIngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # this is automagically passed to arguments of post and delete methods
    lookup_field = "ingredient_id"
    
    def get_queryset(self):
        currentUser = self.request.user
        queryset = UserIngredient.objects.filter(user=currentUser)
        return queryset

    def post(self, request, ingredient_id):
        user = request.user
        userIngredient = user.ingredients.filter(ingredient_id=ingredient_id, user_id=user.id)

        # look into the UniqueTogether validator on this model to prevent multiple entries https://www.django-rest-framework.org/api-guide/validators/#uniquetogethervalidator
        if (not userIngredient):
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            addedIngredient = UserIngredient.objects.create(user=user, ingredient=ingredient, quantity=0, unit="none")
            return JsonResponse(UserIngredientSerializer(addedIngredient).data, safe=False)
        else:
            return JsonResponse("failed", safe=False)

    def destroy(self, request, ingredient_id):
        user = request.user
        ingredientToRemove = user.ingredients.filter(ingredient_id=ingredient_id, user_id=user.id)

        if (ingredientToRemove):
            removedIngredient = UserIngredient.objects.get(user_id=user.id, ingredient_id=ingredient_id)
            ingredientToRemove.delete()
            return JsonResponse(UserIngredientSerializer(removedIngredient).data, safe=False)
        else:
            return JsonResponse("{failed: 'failed'}", safe=False)
        
class AvailableRecipesViewset(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Get all ingredients the user has
        currentUser = self.request.user
        userIngredientIds = UserIngredient.objects.filter(user=currentUser).values_list('ingredient_id', flat=True)

        # For performance, find all the ingredients the user does not have
        inner_queryset = RecipeIngredient.objects.exclude(ingredient_id__in = userIngredientIds)

        # Exclude all recipes where the user does not have the ingredient
        queryset = Recipe.objects.exclude(recipeingredient__in = inner_queryset)

        return queryset