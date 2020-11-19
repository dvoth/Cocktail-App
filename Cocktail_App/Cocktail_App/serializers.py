from rest_framework import serializers
from Cocktail_App.models import *
from rest_framework_recursive.fields import RecursiveField

class IngredientTypeSerializer(serializers.ModelSerializer):
    parentType = RecursiveField(allow_null=True)

    class Meta:
        model = IngredientType
        fields = ['name', 'parentType']

class IngredientSerializer(serializers.ModelSerializer):
    ingredientType = IngredientTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'ingredientType']
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False, read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'measure', 'unit', 'note']

class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['id', 'recipe', 'description', 'order']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)
    steps = RecipeStepSerializer(source='recipestep_set', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'steps', 'ingredients']       