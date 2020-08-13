from django.contrib import admin
from django.urls import path
from recommend import views

app_name = 'recommend'
urlpatterns = [
  path('home/', views.HomeView.as_view(), name='home'),
  path('anime_index/', views.AnimeListView.as_view(), name='anime_index'),
  path('anime_detail/<int:pk>', views.AnimeDetailView.as_view(), name='anime_detail'),
  #path('anime_create/', views.anime_create.as_view(), name='anime_create'),
  #path('anime_update/<int:pk>', views.AnimeUpdateView.as_view(), name='anime_update'),
  #path('anime_delete/<int:pk>', views.AnimeDeleteView.as_view(), name='anime_delete'),
  path('rating_index/', views.RatingListView.as_view(), name='rating_index'),
  path('rating_detail/<int:pk>', views.RatingDetailView.as_view(), name='rating_detail'),
  path('rating_create/<int:pk>', views.RatingCreateView.as_view(), name='rating_create'),
  path('rating_update/<int:pk>', views.RatingUpdateView.as_view(), name='rating_update'),
  path('rating_delete/<int:pk>', views.RatingDeleteView.as_view(), name='rating_delete'),
  path('result_index/', views.ResultListView.as_view(), name='result_index'),
  path('result_detail/<int:pk>', views.ResultDetailView.as_view(), name='result_detail'),
  path('resultKNN_index/', views.ResultKNNListView.as_view(), name='resultKNN_index'),
  path('resultKNN_detail/<int:pk>', views.ResultKNNDetailView.as_view(), name='resultKNN_detail'),
]