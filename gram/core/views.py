from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post, Image
from .forms import AddPostForm, ImageForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



@login_required()
def feed(request, personal_feed=None):
    user = request.user
    if personal_feed:
        posts = Post.objects.filter(author__in=user.profile.following.all()).order_by('-pk')
    else:
        posts = Post.objects.all().order_by('-pk')
    images = Image.objects.all()
    context = {
        'posts': posts,
        'images': images,
        'user': user,
        'feed_topic': f'Feed {personal_feed}'
    }
    return render(request, "core/feed.html", context)


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_obj = get_object_or_404(Post, id=request.POST.get('post_id'))
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
            is_liked = False
        else:
            post_obj.likes.add(user)
            is_liked = True
        data = {
            "total_likes": post_obj.likes.all().count(),
            "is_liked": is_liked}
        return JsonResponse(data, safe=False)


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
