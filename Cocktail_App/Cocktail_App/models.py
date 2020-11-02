from django.db import models

UNITS = [
    ('tsp', 'teaspoon'),
    ('tbsp', 'tablespoon'),
    ('fl oz', 'fluid ounce'),
    ('cup', 'cup'),
    ('pint', 'pint'),
    ('quart', 'quart'),
    ('gallon', 'gallon'),
    ('ml', 'milliter'),
    ('l', 'liter'),
    ('lb', 'pound'),
    ('oz', 'ounce'),
    ('mg', 'milligram'),
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('dashes', 'dashes')
]

class IngredientType(models.Model):
    name = models.CharField(max_length=32)
    parentType = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class  Ingredient(models.Model):
    name = models.CharField(max_length=32)
    ingredientType = models.ForeignKey(IngredientType, on_delete=models.CASCADE)

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length = 1000)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.DecimalField(decimal_places=3, max_digits=5)
    unit = models.CharField(max_length=32, choices=UNITS, null=True)
    note = models.CharField(max_length=32, null=True)

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    order = models.IntegerField()