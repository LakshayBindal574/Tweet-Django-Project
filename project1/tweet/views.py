from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm


def tweet_list(request):
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet/tweet_list.html', {'tweets': tweets, 'query': query})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet created successfully!")
            return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet/tweet_form.html', {'form': form})


@login_required
def tweet_update(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if tweet.user != request.user:
        messages.error(request, "You are not authorized to update this tweet.")
        return redirect('tweet_list')

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Tweet updated successfully!")
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet/tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if tweet.user != request.user:
        messages.error(request, "You are not authorized to delete this tweet.")
        return redirect('tweet_list')

    if request.method == "POST":
        tweet.delete()
        messages.success(request, "Tweet deleted successfully!")
        return redirect('tweet_list')

    return render(request, 'tweet/tweet_delete.html', {'tweet': tweet})


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('tweet_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('tweet_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    username = request.user.username if request.user.is_authenticated else ""
    auth_logout(request)
    if username:
        messages.success(request, f"Goodbye {username}, you have been logged out successfully!")
    else:
        return render(request, 'registration/logout.html')
    return redirect('tweet_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('tweet_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}!")
            return redirect('tweet_list')
        else:
            messages.error(request, "Failed to register. Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})
