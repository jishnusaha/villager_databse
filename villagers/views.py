from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from .models import Villager, Bari
from django.http import HttpResponse, HttpResponseRedirect
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

    paginator = Paginator(villager_list, 3)
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


class VillagerCreateForm(ModelForm):
    class Meta:
        model = Villager
        fields = '__all__'


def create(request):
    if request.method == 'POST':
        form = VillagerCreateForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            villager = Villager()
            villager.name = form.cleaned_data['name']
            villager.sex = form.cleaned_data['sex']
            villager.bari = form.cleaned_data['bari']
            villager.marital_status = form.cleaned_data['marital_status']
            villager.lives_in_village = form.cleaned_data['lives_in_village']
            villager.alive = form.cleaned_data['alive']

            try:
                villager.father = form.cleaned_data['father']
            except:
                pass
            try:
                villager.mother = form.cleaned_data['mother']
            except:
                pass
            try:
                villager.grand_father = form.cleaned_data['grand_father']
            except:
                pass
            try:
                villager.highest_education = form.cleaned_data['highest_education']
            except:
                pass
            try:
                villager.highest_education_institute = form.cleaned_data['highest_education_institute']
            except:
                pass
            try:
                villager.occupation = form.cleaned_data['occupation']
            except:
                pass
            # saving data
            villager.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('villager-details', kwargs={'pk': villager.id}))

    else:
        form = VillagerCreateForm()

    context = {
        'form': form
    }
    return render(request, 'villagers/villager_create.html', context=context)


