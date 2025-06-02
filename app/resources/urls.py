from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("resource/list", views.resource_list, name="resource_list"),
    path("accounts/signup/", views.signup, name="signup"),
    path("upload/", views.upload_resource, name="upload_resource"),
    path('resource/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resource/<int:pk>/edit/', views.edit_resource, name='resource_edit'),
    path('resource/<int:pk>/delete/', views.delete_resource, name='resource_delete'),
    path('resources/pending/', views.pending_resources, name='pending_resources'),
    path('resources/<int:pk>/approve/', views.approve_resource, name='approve_resource'),
    path('resource/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('accounts/profile/', views.profile_view, name='profile_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   