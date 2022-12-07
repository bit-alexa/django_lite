from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post, Image, Like
from .forms import AddPostForm, ImageForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required()
def feed(request):
    posts = Post.objects.all().order_by('-pk')
    images = Image.objects.all()
    user = request.user
    context = {
        'posts': posts,
        'images': images,
        'user': user
    }
    return render(request, "core/feed.html", context)


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_obj = get_object_or_404(Post, id=request.POST.get('post_id'))
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_obj.id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return HttpResponseRedirect(request.POST.get('next', '/'))


def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            for i in files:
                Image.objects.create(post=f, image=i)
            form.save_m2m()
            return redirect('feed')
        else:
            return redirect('feed')
    else:
        form = AddPostForm()
        imageform = ImageForm()
        return render(request, "core/add_post.html", {"form": form, "imageform": imageform})


class TagView(ListView):
    model = Post
    template_name = 'core/feed.html'
    ordering = ['-post_date']
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        first_post = Post.objects.filter(tags__slug=self.kwargs.get('tag_slug')).first()
        context['first_post'] = first_post
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))
