from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review #imports movie model
from django.contrib.auth.decorators import login_required
def index(request):
    search_term = request.GET.get('search') # search bar, retreive value
    if search_term: # if search term not empty
        movies = Movie.objects.filter(name__icontains=search_term) # filter movies where name contains term
        #_icontains used for case-insensitive containment
    else: # empty search term
        movies = Movie.objects.all() # retrieve all movies from database no filters
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies # to render the selected movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id) # get specific movie based on id
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required #ensure only accessed by authenticated users
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.reported = False
        review.report = ""
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if review.reported:
        #redirect to pop up page stating review is under review for violation of policies
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Report Review'
        template_data['review'] = review
        return render(request, 'movies/report_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.reported = True
        review.report = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
