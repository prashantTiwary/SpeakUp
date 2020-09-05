from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt



from .models import User,Post,textForm,Likes


def index(request):
    if request.method == 'POST':
        form = textForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = User.objects.get(id=request.user.id)
            post.save()
            return HttpResponseRedirect(reverse('index'))

    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    try:
        likes = request.user.user.all().values_list('post', flat=True)
    except:
        likes = []    

    return render(request, "network/index.html", {
        'textForm': textForm(),
        'page_obj': page_obj,
        'likes':likes
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




def user(request, id):

    target_user = User.objects.get(id=id)
 
    posts = Post.objects.filter(user=target_user).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)


    try:
        likes = request.user.user.all().values_list('post', flat=True)
    except:
        likes = []      

    return render(request, "network/user.html", {
        'target_user': target_user,
        'page_obj': page_obj,
        'textForm': textForm(),
        'likes': likes
        
    })


@csrf_exempt
@login_required
def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(pk=data['id'])
        try:
            Likes.objects.get(user=request.user, post=post).delete()
            return JsonResponse({
                'liked': False
            })
        except:
            like = Likes(user=request.user, post=post)
            like.save()
            return JsonResponse({
                'liked': True
            })
    else:
        return HttpResponseRedirect(reverse('index'))        


@csrf_exempt
def follow(request, id):
    target_user = User.objects.get(id=id)

    if request.user in target_user.followers.all():
        
        target_user.followers.remove(request.user)
        target_user.save()

        return JsonResponse({"message": f'{id} unfollowed!'})

    target_user.followers.add(request.user)
    target_user.save()

    return JsonResponse({"message": f'{id} followed!'})


@login_required
def following(request):
    post_fetched = Post.objects.order_by("-timestamp").all()

    posts = [] 
    for post in post_fetched:
        
        if post.user in request.user.following.all():
            posts.append(post)

    paginator = Paginator(posts, 10)

    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def edit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Must use PUT method"}, status=400)

    data = json.loads(request.body)
    
    text = data.get("text", "")
    post = Post.objects.get(pk=data['id'])

    if post.user != request.user:
         return JsonResponse({"error": "Can't edit another user's post"}, status=403)

    post.text = text
    post.save()

    return JsonResponse({"message": "Post edited!"}, status=200)
    