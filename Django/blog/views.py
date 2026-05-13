from django.shortcuts import render, redirect
from django.conf import settings
from .forms import PostForm
#import models inside the app
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
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