from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='villagers-list'),
    path('test/', views.test, name='test'),
    path('<int:pk>/', views.detail, name='villager-details')

]