from django.shortcuts import render, get_object_or_404
from dogs.models import Dog, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from dogs.forms import DogForm

def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }

    return render(request, 'dogs/index.html', context)


def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Питомник - Все наши породы'
    }

    return render(request, 'dogs/categories.html', context)


def category_dogs(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': 'Питомник - собаки породы ' + category_item.name,
        'category_pk': category_item.pk,
    }

    return render(request, 'dogs/dogs.html', context)


def dogs_list_view(request):
    context = {
        'object_list': Dog.objects.all(),
        'title': 'Питомник - Все наши собаки'
    }

    return render(request, 'dogs/dogs.html', context)


def dog_create_view(request):
    form = DogForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))

    return render(request, 'dogs/create.html', {'form':DogForm()})