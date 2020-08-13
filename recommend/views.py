from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from recommend.models import Result, ResultKNN, Anime, Rating
from recommend.forms import AnimeForm, RatingForm

import recommend.utils as utils

class HomeView(TemplateView):
  template_name = 'recommend/home.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_id'] = self.request.user.id
    reult_list = Result.objects.filter(user_id=self.request.user.id)
    context['result_one'] = reult_list[0]
    context['result_one'].photo = utils.download_img(context['result_one'].anime_id.name)
    context['result_list'] = reult_list[1:]

    return context

class AnimeListView(LoginRequiredMixin, ListView):
  model = Anime
  template_name = 'recommend/anime_index.html'
  paginate_by = 20

  def get_queryset(self):
    q_word = self.request.GET.get('query')

    if q_word:
      object_list = Anime.objects.filter(Q(name__icontains=q_word) | Q(genre__icontains=q_word))
    else:
      object_list = Anime.objects.all()
    return object_list

class AnimeDetailView(LoginRequiredMixin, DetailView):
  model = Anime
  template_name = 'recommend/anime_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す 
    context["image"] = utils.download_img(context["anime"].name)

    obj = Rating.objects.filter(user_id=self.request.user.id, anime_id=Anime.objects.get(anime_id=str(self.kwargs.get("pk"))))

    if obj:
      context["id_status"] = Rating.objects.get(user_id=self.request.user.id, anime_id=Anime.objects.get(anime_id=str(self.kwargs.get("pk")))).id
      context["db_status"] = False
    else:
      context["form"] = AnimeForm()
      context["db_status"] = True

    return context

class AnimeCreateView(LoginRequiredMixin, CreateView):
  model = Rating
  form_class = RatingForm
  template_name = "recommend/anime_create.html"
  success_url = "/recommend/home"

class AnimeUpdateView(LoginRequiredMixin, UpdateView):
  model = Anime
  form_class = AnimeForm
  template_name = "recommend/anime_update.html"
  success_url = "/recommend/anime_index"

class AnimeDeleteView(LoginRequiredMixin, DeleteView):
  model = Anime
  form_class = AnimeForm
  success_url = "/recommend/anime_index"

  def delete(self, request, *args, **kwargs):
    result = super().delete(request, *args, **kwargs)
    messages.success(self.request, "アニメを削除しました")
    return result

class RatingListView(LoginRequiredMixin, ListView):
  model = Rating
  template_name = 'recommend/rating_index.html'
  paginate_by = 20

  def get_queryset(self):
    return Rating.objects.filter(user_id=self.request.user.id)

class RatingDetailView(LoginRequiredMixin, DetailView):
  model = Rating
  template_name = 'recommend/rating_datail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if str(self.request.user.id) != context['rating'].user_id:
      context['rating'] = Rating()
    return context

class RatingCreateView(LoginRequiredMixin, CreateView):
  model = Rating
  form_class = RatingForm
  template_name = "recommend/rating_create.html"
  success_url = "/recommend/anime_index"

  def form_valid(self, form):
    # テーブルを置く
    user_id = self.request.user.id
    anime = Anime.objects.get(anime_id=str(self.kwargs.get("pk")))

    if Rating.objects.filter(user_id=user_id, anime_id=anime.anime_id):
      messages.warning(self.request, "「" + anime.name + "」はすでに評価されています。" )
    else:
      form.instance.user_id = user_id
      form.instance.anime_id = anime
      messages.success(self.request, "「" + anime.name + "」に評価を投稿しました。" )
    return super(RatingCreateView, self).form_valid(form)

class RatingUpdateView(LoginRequiredMixin, UpdateView):
  model = Rating
  form_class = RatingForm
  template_name = "recommend/rating_update.html"
  success_url = "/recommend/rating_index"

  def form_valid(self, form):
    self.object = post = form.save()
    messages.success(self.request, "「" + Rating.objects.get(id=str(self.kwargs.get("pk"))).anime_id.name + "」の評価を更新しました。" )
    return redirect(self.get_success_url())

class RatingDeleteView(LoginRequiredMixin, DeleteView):
  model = Rating
  form_class = RatingForm
  success_url = "/recommend/rating_index"

  def delete(self, request, *args, **kwargs):
    result = super().delete(request, *args, **kwargs)
    messages.success(self.request, "評価値を削除しました")
    return result

class ResultListView(LoginRequiredMixin, ListView):
  model = Result
  template_name = 'recommend/result_index.html'
  paginate_by = 20

  def get_queryset(self):
    return Result.objects.filter(user_id=self.request.user.id)

class ResultDetailView(LoginRequiredMixin, DetailView):
  model = Result
  template_name = 'recommend/result_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if str(self.request.user.id) != context['result'].user_id:
      context['result'] = Result()
    return context

class ResultKNNListView(LoginRequiredMixin, ListView):
  model = ResultKNN
  template_name = 'recommend/result_index.html'
  paginate_by = 20

  def get_queryset(self):
    return ResultKNN.objects.filter(user_id=self.request.user.id)

class ResultKNNDetailView(LoginRequiredMixin, DetailView):
  model = ResultKNN
  template_name = 'recommend/result_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if str(self.request.user.id) != context['result'].user_id:
      context['result'] = ResultKNN()
    return context