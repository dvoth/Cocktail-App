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
        fields = ['id', 'name', 'ingredientType', 'image']
        
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
        fields = ['id', 'name', 'description', 'steps', 'ingredients', 'image']

class UserSerializer(serializers.ModelSerializer):
    shoppingList = serializers.PrimaryKeyRelatedField(many=True, queryset=ShoppingListItem.objects.all())
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipe.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'shoppingList', 'ingredients', 'recipes']

class UserIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model=UserIngredient
        fields = ['id', 'ingredient', 'user', 'quantity', 'unit']