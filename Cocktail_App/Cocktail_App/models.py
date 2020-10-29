from django.db import models

UNITS = ['tsp', 'tbsp', 'fl oz', 'cup', 'pint', 'quart', 'gallon', 'ml', 'l', 'lb', 'oz', 'mg', 'g', 'kg']

class  Ingredient(models.model):
    name = model.CharField(max_length=32)
    ingredientType = models.ForeignKey(IngredientType, on_delete=models.CASCADE)

class IngredientType(models.model):
    name = model.CharField(max_length=32)
    parentType = models.ForeignKey('self', on_delete=models.CASCADE)

class Recipe(models.model):
    name = model.CharField(max_length=150)
    description = model.TextField(max_length = 1000)

class RecipeIngredient(models.model):
    ingredients = models.ManyToManyField(Ingredient)
    measure = models.DecimalField()
    unit = models.CharField(choices=UNITS)
    note = models.CharField(max_length=32)

class RecipeSteps(models.model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    description = models.CharField(max_length=1000)
    order = models.IntegerField(max_length=2)