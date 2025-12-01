"""
URL configuration for zerazone project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
import os
def serve_sitemap(request):
    # Path to sitemap in root directory
    sitemap_path = os.path.join(settings.BASE_DIR, 'sitemap.xml')
    
    # Read and return the file
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
    
    return HttpResponse(
        content=sitemap_content,
        content_type='application/xml'
    )

def robots_txt(request):
    content = """
    User-agent: *
    Disallow:
    Sitemap: https://www.zerazone.com/sitemap.xml
    """
    return HttpResponse(content, content_type="text/plain")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('sitemap.xml', serve_sitemap, name='serve_sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)