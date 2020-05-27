from django.shortcuts import render, get_object_or_404
from .models import Villager, Bari
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    bari = request.GET.get('bari')
    lives_in_village = request.GET.get('lives_in_village')

    villager_list = Villager.objects.all()
    if bari:
        villager_list = villager_list.filter(bari__name=bari)
    if lives_in_village:
        villager_list = villager_list.filter(lives_in_village=lives_in_village)

    page = request.GET.get('page', 1)

    paginator = Paginator(villager_list, 5)
    try:
        villagers = paginator.page(page)
    except PageNotAnInteger:
        villagers = paginator.page(1)
    except EmptyPage:
        villagers = paginator.page(paginator.num_pages)

    bari_list = Bari.objects.all()
    lives_in_village_list = Villager.objects.values('lives_in_village').distinct()
    print(lives_in_village_list)
    print(bari_list)
    context = {
        'villager_list': villagers,
        'bari_list': bari_list,
        'lives_in_village_list': lives_in_village_list
    }

    return render(request, 'villagers/villagers_list.html', context=context)


def detail(request, pk):
    villager = get_object_or_404(Villager, pk=pk)
    if villager.sex == 'Male':
        children = Villager.objects.filter(father=villager)
    else:
        children = Villager.objects.filter(mother=villager)

    context = {
        'villager': villager,
        'children': children,
    }
    return render(request, 'villagers/villager_details.html', context={'context': context})


def test(request):
    return render(request, 'villagers/test.html')

