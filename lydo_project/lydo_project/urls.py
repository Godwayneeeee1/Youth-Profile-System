"""
URL configuration for lydo_project.
"""
from django.contrib import admin
from django.urls import path
from monitoring import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('reports/', views.reports_page, name='reports_list'),
    path('heatmap/', views.heatmap_page, name='heatmap_page'),
    path('reports/<int:bid>/', views.reports_page, name='reports_by_barangay'),

    path('api/login/', views.login_view, name='login'),
    path('api/register/', views.register_view, name='register'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/user/', views.user_info_view, name='user_info'),

    path('api/barangays/', views.barangays_api, name='barangays_api'),
    path('api/barangay_summary/<int:bid>/', views.barangay_summary, name='barangay_summary'),
    path('api/demographics/', views.demographics_api, name='demographics_api'),
    path('api/heatmap/', views.heatmap_api, name='heatmap_api'),
    path('api/unemployed_heatmap/', views.unemployed_heatmap_api, name='unemployed_heatmap_api'),
    path('api/forms/youth-profile/<int:bid>/', views.download_barangay_blank_form, name='download_barangay_blank_form'),
    path('api/forms/youth-profile-pack/', views.download_blank_form_pack, name='download_blank_form_pack'),

    path('api/youth/', views.youth_api, name='youth_api'),
]
