from . import views
from django.urls import path

urlpatterns = [
    path('',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('projects', views.project_list, name='projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
        path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
     path('download-project-abstract/', views.download_project_abstract, name='download_project_abstract'),
]

