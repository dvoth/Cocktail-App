from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from Cocktail_App import views

router = DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include(router.urls)),
]

# urls for serving images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)