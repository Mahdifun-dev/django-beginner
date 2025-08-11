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
    path('accounts/profile/', views.ProfileDetailView, name='profile_view'),
    path('accounts/profile/', views.Profile, name='profile_view'),
    path('accounts/profile/<str:username>/', views.profile_view, name='other_profile_view'),
    path('profile/add-skill/', views.add_skill, name='add_skill'),
    path('skills/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    path('achievements/add/', views.add_Achievement, name='add_achievement'),
    path('achievements/<int:achievement_id>/delete/', views.delete_Achievement, name='delete_achievement'),
    path('certificates/add/', views.add_Certificate, name='add_certificate'),
    path('certificates/<int:certificate_id>/delete/', views.delete_Certificate, name='delete_certificate'),
    path('educations/add/', views.add_Education, name='add_education'),
    path('educations/<int:education_id>/delete/', views.delete_Education, name='delete_education'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('copyright/', views.copyright, name='copyright'),
    path('report/', views.report, name='report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)