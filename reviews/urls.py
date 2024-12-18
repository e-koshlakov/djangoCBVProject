from django.urls import path
from reviews.apps import ReviewsConfig
from reviews.views import ReviewListView, DogReviewListViewAll, DogReviewDetailView, DogReviewCreateView, \
    ReviewUpdateView, DogReviewDeleteView, review_toggle_activity

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='list_reviews'),
    path('deactivated/', DogReviewListViewAll.as_view(), name='deactivated_reviews'),
    path('review/detail/<slug:slug>/', DogReviewDetailView.as_view(), name='detail_review'),
    path('review/create/', DogReviewCreateView.as_view(), name='create_review'),
    path('review/update/<slug:slug>/', ReviewUpdateView.as_view(), name='update_review'),
    path('review/delete/<slug:slug>/', DogReviewDeleteView.as_view(), name='delete_review'),
    path('review/toogle/<slug:slug>/', review_toggle_activity, name='toggle_activity_review'),
]
