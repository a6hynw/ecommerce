from django.urls import path
from . import views

urlpatterns = [
    # Customer flows
    path('', views.home_view, name='home'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.cart_add_view, name='cart_add'),
    path('cart/update/', views.cart_update_view, name='cart_update'),
    path('cart/remove/', views.cart_remove_view, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Admin flows
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/add-product/', views.admin_add_product, name='admin_add_product'),
    path('admin/edit-product/<int:id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin/delete-product/<int:id>/', views.admin_delete_product, name='admin_delete_product'),
    path('admin/update-order/<int:id>/', views.admin_update_order_status, name='admin_update_order_status'),

    # Super Admin flows
    path('super-admin-dashboard/', views.super_admin_dashboard_view, name='super_admin_dashboard'),
    path('super/add-category/', views.super_add_category, name='super_add_category'),
    path('super/edit-category/<int:id>/', views.super_edit_category, name='super_edit_category'),
    path('super/delete-category/<int:id>/', views.super_delete_category, name='super_delete_category'),
    path('super/user-role/<int:id>/', views.super_manage_user_role, name='super_manage_user_role'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
