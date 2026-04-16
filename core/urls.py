from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.admin import admin_site

# Configuration de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Bancaire",
        default_version='v1',
        description="API pour gérer les utilisateurs d'un système bancaire",
        contact=openapi.Contact(email="contact@api-bancaire.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]