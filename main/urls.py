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
    
    # Custom Admin Panel
    path('custom-login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('dashboard/', views.DashboardView.as_view(), name='custom_dashboard'),
    path('dashboard/projects/', views.AdminProjectListView.as_view(), name='admin_projects'),
    path('dashboard/downloads/', views.AdminDownloadListView.as_view(), name='admin_downloads'),
    path('dashboard/create-project/', views.CreateProjectView.as_view(), name='create_project'),
    path('dashboard/export-records/', views.export_records_csv, name='export_records_csv'),
]

