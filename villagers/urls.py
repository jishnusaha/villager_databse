from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='villagers-list'),
    # path('get/', get_villager, name='get-villager'),
    path('get/', VillagerListView.as_view(), name='get-villager'),
    path('test/', test, name='test'),
    path('add-villager/', create_villager, name='villager-create'),
    path('<int:pk>/add-more-information/', add_more_information_villager, name='villager-add-more-info'),
    path('<int:pk>/edit/', update_villager, name='villager-edit'),
    path('add-bari/', create_bari, name='bari-create'),
    path('<int:pk>/', detail, name='villager-details'),


    path('webhook/', webhook),
    path('webhook/data/', webhook),
    path('https:/6d3470ce8e7e.ngrok.io/webhook/', webhook),
    path('https://6d3470ce8e7e.ngrok.io/webhook/', webhook),

]

