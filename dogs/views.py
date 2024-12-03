from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from dogs.models import Dog, Category
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dogs.forms import DogForm
from django.contrib.auth.mixins import LoginRequiredMixin


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


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')
    extra_context = {'title': 'Добавление питомца'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    extra_context = {'title': 'Питомник - Информация о собаке'}


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {'title': 'Редактирование питомца'}

    def get_success_url(self):
        return reverse('dogs:detail_dog', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return self.object


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    extra_context = {'title': 'Удаление питомца'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return self.object