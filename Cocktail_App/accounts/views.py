from rest_framework import viewsets
from django.http import JsonResponse

from Cocktail_App.models import Ingredient
from accounts.models import UserIngredient
from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.serializers import UserIngredientSerializer

# Create your views here.
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
