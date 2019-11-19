from django.shortcuts import render, redirect
from .forms import ProfileForm,ImageForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile,Comments,Likes
 

@login_required(login_url='/accounts/login/')
def index(request):
    posts = Image.get_all_images()
    profile = Profile.get_all_profiles()
    comments=Comments.objects.all()
#     current_user = request.user
#     if request.method == 'POST':
#         form = CommentForm(request.POST, request.FILES)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = current_user
#             comment.save()
#         return redirect('index')
#     else:
        # form=CommentForm()
    context =  {
        "profile": profile,
        # "form": form,
        "posts":posts ,
        # "comments":comments,
        }
    return render(request, 'istagram/index.html', context)
    
@login_required(login_url='/accounts/login/')
def add_image(request):
        current_user = request.user
        if request.method == 'POST':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('index')
        else:
                form = ImageForm()
                return render(request,'istagram/image.html', {"form":form})

@login_required(login_url='/accounts/login/')                
def profile_info(request):
        current_user = request.user
        follow = len(Follow.objects.followers(users))
        following = len(Follow.objects.following(users))
        people_following = Follow.objects.following(request.user)
        profile = Profile.objects.filter(user=current_user).first()
        posts = request.user.image_set.all()
       
        return render(request, 'istagram/profile.html', {"images": posts, "profile": profile, 'follow':follow, 'following':following,'people_following':people_following})
@login_required(login_url='/accounts/login/') 
def profile_update(request):
         current_user = request.user
         if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('profile')
         else:
                form = ProfileForm()
         return render(request,'istagram/profile_update.html',{"form":form})

@login_required(login_url='/accounts/login/') 
def comment(request,image_id):
        current_user=request.user
        image = Image.objects.get(id=image_id)
        profile_owner = User.objects.get(username=current_user.username)
        comments = Comments.objects.all()
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.image = image
                        comment.comment_owner = current_user
                        comment.save()
            
                       
                return redirect('index')
        else:
                form = CommentForm()
        return render(request, 'istagram/comment.html',{"comments":comments})

@login_required(login_url='/accounts/login/') 
def like(request, image_id):
    current_user = request.user
    image=Image.objects.get(id=image_id)
    new_like,created= Likes.objects.get_or_create(user=current_user, image=image)
    new_like.save()

    return redirect('index')

# def like(request,image_id):
#   image = Image.objects.get(pk = image_id)
#   is_liked = False
#   if image.likes.filter(id = request.user.id).exists():
#       image.likes.remove(request.user)
#       is_liked = False
#   else:
#       image.likes.add(request.user)
#       is_liked = True
#   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username__icontains = search_term)
        message = f"{search_term}"
        profile_pic = User.objects.all()
        return render(request, 'search.html', {'message':message, 'users':searched_users, 'profile_pic':profile_pic})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {'message':message})

def follow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('index')

def unfollow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('index')