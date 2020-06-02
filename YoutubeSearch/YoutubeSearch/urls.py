from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('McViewer.urls')),

    path('', TemplateView.as_view(template_name='base.html')),
] + static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)
