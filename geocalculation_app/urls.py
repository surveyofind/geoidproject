
from django.urls import path
from.import views

urlpatterns = [
    path('',views.login_view,name='login_view'),
    path('signup_view',views.signup_view,name='signup_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('geoid_dashboard',views.geoid_dashboard,name='geoid_dashboard'),
    path('geoid_valuefind',views.geoid_valuefind,name='geoid_valuefind'),
    path('download_csv/', views.download_processed_csv, name='download_csv'),
    path('download_points/', views.download_points, name='download_points'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin_dasboard/', views.admin_dasboard, name='admin_dasboard'),
    path('approve_users', views.approve_users, name='approve_users'),
    path('edit/<int:id>/', views.edituser, name='edituser'),
    path('user/update_status/<int:id>/', views.update_user_status, name='update_user_status'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    
    
]
