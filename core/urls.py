from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('scores/', include('scores.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('charities/', include('charities.urls')),
    path('draws/', include('draws.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)