from rest_framework import viewsets
from accounts.models import UserIngredient
from Cocktail_App.models import Ingredient
from Cocktail_App.models import Recipe
from Cocktail_App.models import RecipeIngredient
from Cocktail_App.serializers import RecipeSerializer
from Cocktail_App.serializers import IngredientSerializer
from Cocktail_App.permissions import IsAuthenticatedForUnsafeMethods, IsOwnerOrReadOnly

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedForUnsafeMethods]

    # Overriding perform_create just to send the user along to the serializer's validated_data field
    # Need to do this because you can't access the user in the serializer by default
    # https://www.django-rest-framework.org/api-guide/serializers/#passing-additional-attributes-to-save 
    def perform_create(self, serializer):
        # Staff members can decide if the recipe they are adding should be a master recipe
        if ("master_recipe" in self.request.data) and (self.request.data["master_recipe"] is True) and (self.request.user.is_staff):
            # Will not send a user to the serializer, resulting in a null user_id in the database 
            # Null user_id denotes that this is a "master" recipe anyone can access
            serializer.save()
        else:
            serializer.save(user=self.request.user)


