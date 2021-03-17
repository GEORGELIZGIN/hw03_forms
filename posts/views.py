from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Group, Post


def index(request):
    latest = Post.objects.all()[:11]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


class NewPostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    success_url = reverse_lazy('index')
    template_name = 'new_post.html'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()
        return super().form_valid(form)
