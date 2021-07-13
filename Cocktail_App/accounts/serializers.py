from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import ShoppingListItem
from accounts.models import UserIngredient
from accounts.models import User
from Cocktail_App.models import Recipe
from Cocktail_App.serializers import IngredientSerializer

class UserIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False, read_only=True)

    class Meta:
        model=UserIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit']

class UserSerializer(serializers.ModelSerializer):
    ingredients = UserIngredientSerializer(many=True)
    # shoppingList = serializers.PrimaryKeyRelatedField(many=True, queryset=ShoppingListItem.objects.all())
    # recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipe.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'ingredients']
        # fields = ['id', 'username', 'email', 'shoppingList', 'ingredients', 'recipes']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")

    