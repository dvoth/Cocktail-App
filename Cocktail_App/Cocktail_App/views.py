from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from Cocktail_App.models import Ingredient
from Cocktail_App.models import IngredientType
from Cocktail_App.models import Recipe
from Cocktail_App.models import RecipeStep
from Cocktail_App.models import RecipeIngredient
from Cocktail_App.models import UserIngredient
from Cocktail_App.models import User
from Cocktail_App.serializers import IngredientTypeSerializer
from Cocktail_App.serializers import RecipeSerializer
from Cocktail_App.serializers import RecipeStepSerializer
from Cocktail_App.serializers import RecipeIngredientSerializer
from Cocktail_App.serializers import IngredientSerializer
from Cocktail_App.serializers import UserSerializer
from Cocktail_App.serializers import UserIngredientSerializer
from Cocktail_App.permissions import IsOwnerOrReadOnly

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, pk):
        ingredientId = request.data['ingredientId']
        user = User.objects.get(id=pk)
        userIngredient = user.ingredients.filter(ingredient_id=ingredientId, user_id=pk)

        # look into the UniqueTogether validator on this model to prevent multiple entries https://www.django-rest-framework.org/api-guide/validators/#uniquetogethervalidator
        if (not userIngredient):
            ingredient = Ingredient.objects.get(pk=ingredientId)
            addedIngredient = UserIngredient.objects.create(user=user, ingredient=ingredient, quantity=0, unit="none")
            return JsonResponse(UserIngredientSerializer(addedIngredient).data, safe=False)
        else:
            return JsonResponse("failed", safe=False)
