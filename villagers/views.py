import json

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Villager, Bari
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializer import VillagerSerializer
from pprint import pprint


def index(request):
    bari = request.GET.get('bari')
    lives_in_village = request.GET.get('lives_in_village')
    # print('bari: ', bari)
    # print('lives_in_village: ', lives_in_village)
    villager_list = Villager.objects.all().order_by('id')
    if bari:
        villager_list = villager_list.filter(bari__name=bari)
    if lives_in_village:
        villager_list = villager_list.filter(lives_in_village=lives_in_village)

    page = request.GET.get('page', 1)

    paginator = Paginator(villager_list, 15)
    try:
        villagers = paginator.page(page)
    except PageNotAnInteger:
        villagers = paginator.page(1)
    except EmptyPage:
        villagers = paginator.page(paginator.num_pages)

    bari_list = Bari.objects.all()
    lives_in_village_list = Villager.objects.values('lives_in_village').distinct()
    context = {
        'villager_list': villagers,
        'bari_list': bari_list,
        'lives_in_village_list': lives_in_village_list
    }

    return render(request, 'villagers/villagers_list.html', context=context)


class VillagerListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = VillagerSerializer

    def get_queryset(self):
        # print("in villagerlistview")
        name = self.request.query_params.get('name', None)
        bari = self.request.query_params.get('bari', None)
        lives_in_village = self.request.query_params.get('lives_in_village', None)
        # print('name: ', name)
        # print('bari: ', bari)
        # print('lives_in_village: ', lives_in_village)
        queryset = Villager.objects.all().order_by('id')

        if name:
            queryset = queryset.filter(name__icontains=name)
        # else:
        #     print("no filter by name")
        if bari:
            queryset = queryset.filter(bari__name=bari)
        # else:
        #     print("no filter by bari")
        if lives_in_village:
            queryset = queryset.filter(lives_in_village=lives_in_village)
        # else:
        #     print("no filter by lives_in_village")

        # print(queryset)
        return queryset


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
    return render(request, 'villagers/villager_details.html', context=context)


def test(request):
    return render(request, 'villagers/test.html')


class VillagerCreateForm(ModelForm):
    class Meta:
        model = Villager
        fields = ['name', 'sex', 'bari', 'marital_status', 'lives_in_village', 'alive']


@login_required
def create_villager(request):
    if request.method == 'POST':
        form = VillagerCreateForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            instance = form.save()
            if request.POST.get("Save"):
                # redirect to a Details URL:
                return HttpResponseRedirect(reverse('villager-details', kwargs={'pk': instance.id}))
            else:
                return HttpResponseRedirect(reverse('villager-add-more-info', kwargs={'pk': instance.id}))


    else:
        form = VillagerCreateForm()

    context = {
        'form': form
    }
    return render(request, 'villagers/villager_create.html', context=context)


@login_required
def update_villager(request, pk):
    instance = get_object_or_404(Villager, pk=pk)
    form = VillagerCreateForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        if request.POST.get("Save"):
            # redirect to a Details URL:
            print("redirect to details")
            return HttpResponseRedirect(reverse('villager-details', kwargs={'pk': instance.id}))
        else:
            print("redirect to add more")
            return HttpResponseRedirect(reverse('villager-add-more-info', kwargs={'pk': instance.id}))

    return render(request, 'villagers/villager_create.html', context={'form': form})


class VillagerAddMoreInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True

    class Meta:
        model = Villager
        fields = ['name', 'father', 'mother', 'grand_father', 'grand_mother', 'highest_education',
                  'highest_education_institute', 'occupation', 'spouse']


@login_required
def add_more_information_villager(request, pk):
    instance = get_object_or_404(Villager, pk=pk)
    form = VillagerAddMoreInfoForm(request.POST or None, instance=instance)

    object = Villager.objects.exclude(id=instance.id).filter(bari=instance.bari)

    form.fields['father'].queryset = object.filter(sex='Male')
    form.fields['mother'].queryset = object.filter(sex='Female')
    form.fields['grand_father'].queryset = object.filter(sex='Male')
    form.fields['grand_father'].queryset = object.filter(sex='Female')
    if instance.marital_status == 'Unmarried':
        form.fields['spouse'].disabled = True
    else:
        if instance.sex == 'Male':
            form.fields['spouse'].queryset = object.filter(sex='Female')
        else:
            form.fields['spouse'].queryset = object.filter(sex='Male')

    # print(form)
    if form.is_valid():
        instance = form.save()
        if instance.spouse:
            spouse = instance.spouse
            spouse.spouse = instance
            spouse.marital_status = instance.marital_status
            spouse.save()
        else:
            print("no spouse")

        return HttpResponseRedirect(reverse('villager-details', kwargs={'pk': pk}))
    return render(request, 'villagers/villager_add_more_info.html', {'form': form, 'id': pk})


class BariCreateForm(ModelForm):
    class Meta:
        model = Bari
        fields = '__all__'


@login_required
def create_bari(request):
    context = {}
    if request.method == "POST":
        form = BariCreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            context['done'] = f"{instance.name} Added Successfully"
            form = BariCreateForm()
    else:
        form = BariCreateForm()

    context['form'] = form
    return render(request, 'villagers/bari_create.html', context=context)

