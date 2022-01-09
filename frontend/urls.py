from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),

    path('process/<int:order_id>', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('update_info/', views.updates_info, name='updates_info'),

    ]