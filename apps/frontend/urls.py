from django.urls import path

from apps.frontend import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process/<int:order_id>", views.payment_process, name="process"),
    path("done/", views.payment_done, name="done"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("update_info/", views.updates_info, name="updates_info"),
    path('add_cat_onliner/<int:code_add>', views.add_cat_onliner, name='add_cat_onliner'),
]
