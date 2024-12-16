from django.urls import path
from . import views


urlpatterns = [
    path('homepost/<str:user_uid>/<str:username>/', views.HomePost, name='homepost'),
    path('post/<str:user_uid>/<str:username>/', views.PostProducts, name='post_products'),
    path('dashboard/<str:user_uid>/<str:username>/', views.Dashboard, name='mydashboard'),
     path('edit_prod/<str:user_uid>/<str:username>/<str:apt_Id>/', views.Edit, name='edit_product'),
    path('prod_edited/<str:user_uid>/<str:username>/<str:apt_Id>/', views.ProductUpdated, name='product_edited'),
    path('delete_product/<str:user_uid>/<str:username>/<str:apt_Id>/', views.Delete, name='delete'),
    path('deleted/<str:user_uid>/<str:username>/<str:apt_Id>/', views.DeletionProduct, name='prod_deleted'),
    path('cancelled_deletion/<str:user_uid>/<str:username>/', views.CancellDeletion, name='cancelled_deletion'),
]