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

def upload_path(instance, filename):
    # Stores in a path like "/media/Ingredients/Gin/bombay_sapphire.jpg"
    return '/'.join([type(instance).__name__, str(instance.name), filename])

class IngredientType(models.Model):
    name = models.CharField(max_length=32)
    parentType = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    ingredientType = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length = 1000)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)
    
    # If this field is null, it means that the recipe is a "master" recipe provided by default
    # Otherwise it is a custom user recipe
    user = models.ForeignKey('accounts.User', null=True, on_delete=models.CASCADE)

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
