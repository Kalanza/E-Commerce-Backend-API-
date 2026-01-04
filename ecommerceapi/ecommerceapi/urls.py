"""
URL configuration for ecommerceapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView
from orders.views import MpesaCheckoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Swagger/API Documentation Setup
schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API",
        default_version='v1',
        description="Comprehensive E-Commerce Backend API with JWT Authentication",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@ecommerce.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to E-Commerce API',
        'endpoints': {
            'admin': '/admin/',
            'login': '/api/token/',
            'refresh_token': '/api/token/refresh/',
            'register': '/api/register/',
            'products': '/api/products/',
            'categories': '/api/categories/',
            'swagger_docs': '/swagger/',
            'redoc_docs': '/redoc/',
        }
    })


urlpatterns = [
    path("", api_root, name='api_root'),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'), #This is "Login"
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/pay/', MpesaCheckoutView.as_view(), name = 'mpesa_checkout'),
    path('api/', include('products.urls')),
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
