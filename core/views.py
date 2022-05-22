from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login , logout
from .models import Profile, Post, LikePost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def home(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user = request.user)
    return render(request, 'index.html', {'posts':posts})




def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username = username, email = email, password = password )
            user.save()

            user_login = auth.authenticate(username = username, password = password)
            auth.login(request, user_login)

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user = user_model, users_id = user_model.id)
            new_profile.save()
            return redirect('setting')

        else:
            messages.info(request , "Password not matching!!! ")

    else:
        return render(request, 'signup.html')




def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user =authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, "Invalid username and password")


    return render(request, 'signin.html')


@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('profile_pic') == None:
            profile_pic = user_profile.profile_picture
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_picture = profile_pic
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('profile_pic') != None:
            profile_pic = request.FILES.get('profile_pic')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_picture = profile_pic
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('home')
    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        caption = request.POST['caption']
        image = request.FILES.get('image_upload')

        post = Post.objects.create(user = user, caption = caption, picture = image)
        post.save()
        return redirect('home')

    else:
        return render(request, 'index.html') 

@login_required(login_url='signin')
def liked_by(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)

    liked_filter = LikePost.objects.filter(post_id = post_id , username= username).first()

    if liked_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username = username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('home')


    else:
        liked_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('home')


    return render(request, 'index.html')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    profiles = Profile.objects.get(user = user_object)
    posts = Post.objects.filter(user = pk)
    no_of_post = len(posts)
    context = {
        'user_object' :user_object,
        'profiles' :profiles,
        'posts' :posts,
        'no_of_post' :no_of_post
    }
    return render(request, 'profile.html', context)