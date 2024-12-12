from django.urls import path

from . import views

urlpatterns = [
    path("<slug:name_table>/", views.table, name="show_table"),
]
