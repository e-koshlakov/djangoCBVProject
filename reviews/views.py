from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from reviews.models import Review
from reviews.utils import slug_generator
from users.forms import StyleFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from users.models import UserRoles
from reviews.forms import ReviewForm


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    extra_context = {
        'title': 'Список отзывов'
    }
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset.order_by('created')


class DogReviewListViewAll(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews'
    extra_context = {
        'title': 'Список неактивных отзывов'
    }
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class DogReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'


class DogReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/review_create_update.html'
    form_class = ReviewForm

    # fields = ['title', 'content', 'slug', 'sign_of_review', 'author', 'dog']
    # success_url = '/reviews/'
    def form_valid(self, form):
        if self.request.user.role not in [UserRoles.ADMIN, UserRoles.USER]:
            raise PermissionDenied

        self.object = form.save()
        print(f'object: {self.object.slug}')
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
            print(f'object: {self.object.slug}')
            self.object.author = self.request.user
            self.object.save()
            return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'


    def get_success_url(self):
        print(f'kwargs: {self.kwargs}')
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied
        return self.object


class DogReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:list_reviews')


def review_toggle_activity(request, slug):
    review = get_object_or_404(Review, slug=slug)
    if review.author != request.user and request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
        return HttpResponseForbidden

    if review.sign_of_review:
        review.sign_of_review = False
        review.save()
        return redirect('reviews:deactivated_reviews')
    else:
        review.sign_of_review = True
        review.save()
        return redirect('reviews:list_reviews')
