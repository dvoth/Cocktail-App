from django.contrib import admin
from .models import Recipe, Ingredient, IngredientType, RecipeIngredient, RecipeStep

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeStep)