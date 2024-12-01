from django.shortcuts import render, get_object_or_404
from dogs.models import Dog, Category
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dogs.forms import DogForm


def index(request):
    """
    Отображает главную страницу с тремя первыми собаками.

    Аргументы:
        request (HttpRequest): Объект запроса.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном главной страницы.
    """
    context = {
        'object_list': Dog.objects.all()[:3],
        'title': 'Питомник - Главная'
    }

    return render(request, 'dogs/index.html', context)


def categories(request):
    """
    Отображает страницу со всеми категориями пород.

    Аргументы:
        request (HttpRequest): Объект запроса.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы категорий.
    """
    context = {
        'object_list': Category.objects.all(),
        'title': 'Питомник - Все наши породы'
    }

    return render(request, 'dogs/categories.html', context)


def category_dogs(request, pk):
    """
    Отображает страницу с собаками определенной породы.

    Аргументы:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ категории породы.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы собак определенной породы.
    """
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': 'Питомник - собаки породы ' + category_item.name,
        'category_pk': category_item.pk,
    }

    return render(request, 'dogs/dogs.html', context)

class DogsListView(ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {'title': 'Питомник - Все наши собаки'}



def dog_create_view(request):
    """
    Обрабатывает создание новой собаки.

    Аргументы:
        request (HttpRequest): Объект запроса.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы создания собаки или перенаправление на список собак.
    """
    form = DogForm(request.POST, request.FILES)
    if form.is_valid():
        dog_object = form.save()
        dog_object.owner = request.user
        dog_object.save()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    context = {
        'title': 'Добавление питомца',
        'form': DogForm(),
    }

    return render(request, 'dogs/create_update.html', context)


def dog_detail_view(request, pk):
    """
    Отображает страницу с подробной информацией о собаке.

    Аргументы:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ собаки.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы подробной информации о собаке.
    """
    context = {
        'object': get_object_or_404(Dog, pk=pk),
        'title': 'Питомник - Информация о собаке'
    }
    return render(request, 'dogs/detail.html', context)


def dog_update_view(request, pk):
    """
    Обрабатывает обновление информации о собаке.

    Аргументы:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ собаки.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы обновления собаки или перенаправление на страницу подробной информации о собаке.
    """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:detail_dog', args={pk: pk}))

    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object),
        'title': 'Питомник - Обновление информации о собаке'
    }

    return render(request, 'dogs/create_update.html', context)


def dog_delete_view(request, pk):
    """
    Обрабатывает удаление собаки.

    Аргументы:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ собаки.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы удаления собаки или перенаправление на список собак.
    """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))

    return render(request, 'dogs/delete.html', {'object': dog_object})
