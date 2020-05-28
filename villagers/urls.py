from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='villagers-list'),
    path('test/', test, name='test'),
    # path('create/', Create.as_view(), name='villager-create'),
    path('create/', create, name = 'villager-create'),
    path('<int:pk>/', detail, name='villager-details')

]