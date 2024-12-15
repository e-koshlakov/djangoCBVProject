from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from dogs.models import Dog, Category, Parent
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dogs.forms import DogForm, ParentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory

from users.models import UserRoles


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


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dogs/categories.html'
    extra_context = {'title': 'Питомник - Все наши породы'}


class DogCategoryListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {'title': 'Питомник - Все наши собаки'}


class DogsListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {'title': 'Питомник - Все наши собаки'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

class DogDeactivateListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {'title': 'Питомник - неактивные собаки'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
            return queryset
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
            return queryset

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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        contex_data = self.get_context_data()
        formset = contex_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


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

def dog_toggle_activity(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
        if dog.is_active:
            dog.is_active = True
        else:
            dog.is_active = False
        dog.save()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    else:
        raise PermissionDenied