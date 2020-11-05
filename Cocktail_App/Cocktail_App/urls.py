from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Cocktail_App import views

router = DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]