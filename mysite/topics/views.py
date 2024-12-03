from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from .models import Topic, Comment
from .forms import CommentForm, TopicForm, RegisterForm, LoginForm

def topic_list(request):
    topics = Topic.objects.annotate(
        comment_count=Count('comments')
    ).order_by('-created_at')
    return render(request, 'topics/topic_list.html', {'topics': topics})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic.objects.annotate(
        comment_count=Count('comments')), pk=topic_id)
    comments = topic.comments.order_by('created_at')
    comment_form = CommentForm()
    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic = topic
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('topic_detail', topic_id=topic.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, 'You can only delete your own comments!')
        return redirect('topic_detail', topic_id=comment.topic.id)

    topic_id = comment.topic.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('topic_detail', topic_id=topic_id)

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user != topic.author:
        messages.error(request, 'You can only edit your own topics!')
        return redirect('topic_detail', topic_id=topic.id)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'topics/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user != topic.author:
        messages.error(request, 'You can only delete your own topics!')
        return redirect('topic_detail', topic_id=topic.id)

    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted successfully!')
        return redirect('topic_list')
    return render(request, 'topics/delete_topic.html', {'topic': topic})

@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm()
    return render(request, 'topics/create_topic.html', {'form': form})

@login_required
def profile_view(request):
    user_topics = request.user.topics.all()
    user_comments = request.user.comments.all()
    return render(request, 'topics/profile.html', {
        'user_topics': user_topics,
        'user_comments': user_comments
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'topics/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('topic_list')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'topics/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('topic_list')