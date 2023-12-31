"""book_heaven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import handler403, handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('allauth.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('profiles/', include('profiles.urls')),
    path('reviews/', include('reviews.urls')),
    path('admin_panel/', include('admin_panel.urls')),
]

# set url for user uploaded content
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# set url for static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = handler403
handler404 = handler404
handler500 = handler500
