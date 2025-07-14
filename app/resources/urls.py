from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.resource_list, name="home"),
    path("resources/list", views.resource_list, name="resources_list"),
    path("accounts/signup/", views.signup, name="signup"),
    path("upload/", views.upload_resource, name="upload_resource"),
    path('resources/<int:pk>/', views.resource_detail, name='resources_detail'),
    path('resources/<int:pk>/edit/', views.edit_resource, name='resources_edit'),
    path('resources/<int:pk>/delete/', views.delete_resource, name='resources_delete'),
    path('resources/pending/', views.pending_resources, name='resources_pending'),
    path('resources/<int:pk>/approve/', views.approve_resource, name='resources_approve'),
    path('resources/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('accounts/profile/', views.ProfileDetailView.as_view(), name='profile_view'),
    path('profile/add-skill/', views.add_skill, name='add_skill'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)