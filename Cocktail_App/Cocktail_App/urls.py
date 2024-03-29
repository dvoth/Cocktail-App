from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from Cocktail_App import views as cocktail_views
from accounts import views as account_views

router = DefaultRouter()
router.register(r'ingredients', cocktail_views.IngredientViewSet)
router.register(r'recipes', cocktail_views.RecipeViewSet)
router.register(r'user/available-recipes', account_views.AvailableRecipesViewset, basename='available-recipes')
router.register(r'user/ingredients', account_views.UserIngredientsViewSet, basename='ingredients')

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('accounts.urls')),
]

# urls for serving images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)