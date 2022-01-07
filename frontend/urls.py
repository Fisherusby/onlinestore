from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),

    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),

    ]