from django.urls import path 
from firealert import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.home, name="home"),
    path('reloadData/', TemplateView.as_view(template_name='data.html')),
    path("data", views.data, name="data"),
    path("alert", TemplateView.as_view (template_name='alert.html')),
    path("alertData/", views.alertdata, name="alertdata"),
    path("zip/", views.zip, name="zip"),
    ]