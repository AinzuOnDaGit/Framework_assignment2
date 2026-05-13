from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q # allows or/and/not queries in Django
from .forms import PostForm
#import models inside the app
from .models import Post

# Create your views here.
def index(request):
    # retrieve the search item from the "Filter" parameter
    query = request.GET.get("Filter")

    if query:
        # use Q to allow OR logic
        # title or description contains query (passed searched item)
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-id')
    else:
        posts = Post.objects.order_by('id')[:3]
    return render(request, "blog/index.html", {"posts": posts})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = PostForm()

    return render(request, "blog/create.html", {"form": form})