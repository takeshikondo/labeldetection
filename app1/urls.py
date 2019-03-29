from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('upload2', views.upload2, name='upload2'),
    path('download', views.download, name='download'),
]