from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin_register',views.admin_register,name='admin_register'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_choice',views.admin_choice,name='admin_choice'),
    path('admin_view_all_records',views.admin_view_all_records,name='admin_view_all_records'),
    path('admin_view_all_reply',views.admin_view_all_reply,name='admin_view_all_reply'),
    path('admin_view_manager_detail',views.admin_view_manager_detail,name='admin_view_manager_detail'),
    path('admin_add_manager',views.admin_add_manager,name='admin_add_manager'),
    path('admin_update_manager',views.admin_update_manager,name='admin_update_manager'),
    path('admin_delete_manager',views.admin_delete_manager,name='admin_delete_manager'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('manager_register',views.manager_register,name='manager_register'),
    path('manager_login',views.manager_login,name='manager_login'),
    path('manager_choice',views.manager_choice,name='manager_choice'),
    path('manager_view_feedback',views.manager_view_feedback,name='manager_view_feedback'),
    path('manager_reply_feedback',views.manager_reply_feedback,name='manager_reply_feedback'),
    path('manager_logout',views.manager_logout,name='manager_logout'),
    path('customer_register',views.customer_register,name='customer_register'),
    path('customer_login',views.customer_login,name='customer_login'),
    path('customer_choice',views.customer_choice,name='customer_choice'),
    path('customer_submit_feedback',views.customer_submit_feedback,name='customer_submit_feedback'),
    path('customer_view_feedback',views.customer_view_feedback,name='customer_view_feedback'),
    path('cust_delete_feedback',views.cust_delete_feedback,name='cust_delete_feedback'),
    path('cust_edit_feedback',views.cust_edit_feedback,name='cust_edit_feedback'),
    path('customer_view_feedback_reply',views.customer_view_feedback_reply,name='customer_view_feedback_reply'),
    path('review.html',views.review,name='review.html'),
    path('customer_logout',views.customer_logout,name='customer_logout'),

]