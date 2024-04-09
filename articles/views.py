from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, FormView
from .models import Article
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import CommentForm
from django.views import View
# Create your views here.


#list view
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles' #object name 
    
#detail view 
class CommentGet(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'object'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context 
    
class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = 'article_detail.html' 
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})

class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view() #type: ignore
        return view(request, *args, **kwargs)

#edit view
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields =( "title", "body")
    template_name = 'article_edit.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user  # type: ignore


#delete view 
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy("articles")
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user # type: ignore
    
#create new articles views
class ArticlesCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body') 
    context_object_name = 'article_new'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
 

