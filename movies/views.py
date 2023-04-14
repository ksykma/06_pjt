from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import MovieForm, CommentForm
from .models import Movie, Comment

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies':movies
    }
    return render(request, 'movies/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    if not request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:detail', movie.id)
    else:
        form = MovieForm()
    context = {
        'form':form
    }
    return render(request, 'movies/create.html', context)

@require_http_methods(['GET'])
def detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie':movie,
        'comments':comments,
        'comment_form' : comment_form
    }
    return render(request, 'movies/detail.html', context)

@require_http_methods(['GET', 'POST'])
def update(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.user == request.user:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie_id)
        else:
            form = MovieForm(instance=movie)
        context = {
            'form':form,
            'movie':movie
        }
        return render(request, 'movies/update.html', context)
    return redirect('movies:detail', movie_id)

@require_http_methods(['POST'])
def delete(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect('movies:index')

@require_http_methods(['POST'])
def comments_create(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    movie = Movie.objects.get(id=movie_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
    return redirect('movies:detail', movie_id)

@require_http_methods(['POST'])
def comments_delete(request, movie_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:detail', movie_id)

@require_http_methods(['POST'])
def likes(request, movie_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        if movie.like_users.filter(id=request.user.id).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')