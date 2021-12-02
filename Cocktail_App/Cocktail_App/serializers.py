from rest_framework import serializers
from Cocktail_App.models import *
from django.http import JsonResponse
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
        fields = ['id', 'name', 'ingredientType', 'image']
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    # Not required for creation (we don't want to send a whole ingredient in the API)
    ingredient = IngredientSerializer(many=False, required=False, read_only=False)

    # Manually including so we can just send the ingredient_id in the API on create
    # read_only=false because otherwise the validator would strip this field and we couldn't create recipeingredients
    ingredient_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'measure', 'unit', 'note']

class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['id', 'description', 'order']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)
    steps = RecipeStepSerializer(source='recipestep_set', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'steps', 'ingredients', 'image']

    # DRF does not support creating nested serializers, so we have to manually define it
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    def create(self, validated_data):
        # remove the recipeingredients and recipesteps to manually save these later
        ingredients = validated_data.pop('recipeingredient_set')
        steps = validated_data.pop('recipestep_set')

        # create a recipe without ingredients and steps 
        recipe = Recipe.objects.create(**validated_data)

        # Create the recipe ingredients
        recipeIngredientSerializer = RecipeIngredientSerializer(data=ingredients, many=True)
        recipeIngredientSerializer.is_valid(raise_exception=True)
        recipeIngredientSerializer.save(recipe=recipe)
        
        # Create the recipe steps
        recipeStepSerializer = RecipeStepSerializer(data=steps, many=True)
        recipeStepSerializer.is_valid(raise_exception=True)
        recipeStepSerializer.save(recipe=recipe)

        # Return the recipe, which should have ingredients and steps injected in the RecipeSerializer 
        return recipe
