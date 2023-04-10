from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('apps.users.urls')),
    path('api/pdf/operations/', include('apps.pdf_data_processing.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [ re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]


