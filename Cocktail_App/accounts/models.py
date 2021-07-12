from django.db import models
from django.contrib.auth.models import User

from Cocktail_App.models import Recipe
from Cocktail_App.models import Ingredient
from Cocktail_App.models import UNITS

# Create your models here.
class UserRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    favorited = models.BooleanField()
    lastMade = models.DateField(auto_now=True)

class UserIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ingredients', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=32, choices=UNITS, null=True)

class ShoppingListItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='shoppingList', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=32, choices=UNITS, null=True)
    