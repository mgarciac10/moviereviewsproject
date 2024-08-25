from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Mateo Garcia Carreno'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def statistics_view_movie_year(): 
    matplotlib.use('Agg') 
    all_movies = Movie.objects.all()
 
    movie_counts_by_year = {} 
 
    for movie in all_movies: 
        year = movie.year if movie.year else "None" 
        if year in movie_counts_by_year: 
            movie_counts_by_year[year] += 1 
        else: 
            movie_counts_by_year[year] = 1 
 
    bar_width = 0.5  
    bar_positions = range(len(movie_counts_by_year)) 
 
    # Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center') 
 
    # Personalizar la gráfica 
    plt.title('Movies per year') 
    plt.xlabel('Year') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90) 
 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.3) 
 
    # Guardar la gráfica en un objeto BytesIO 
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
    # Convertir la gráfica a base64 
    image_png = buffer.getvalue() 
    buffer.close() 
    graphic = base64.b64encode(image_png) 
    graphic = graphic.decode('utf-8') 
    return graphic

def statistics_view_movie_genre(): 
    matplotlib.use('Agg') 
    all_movies = Movie.objects.all()
 
    movie_counts_by_genre = {} 
 
    for movie in all_movies: 
        genre = movie.genre if movie.genre else "None" 
        genre = genre.split(',')
        genre = genre[0]
        if genre in movie_counts_by_genre: 
            movie_counts_by_genre[genre] += 1 
        else: 
            movie_counts_by_genre[genre] = 1 
 
    bar_width = 0.5  
    bar_positions = range(len(movie_counts_by_genre)) 
 
    # Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center') 
 
    # Personalizar la gráfica 
    plt.title('Movies per genre') 
    plt.xlabel('Genre') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90) 
 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.5)
 
    # Guardar la gráfica en un objeto BytesIO 
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
    # Convertir la gráfica a base64 
    image_png = buffer.getvalue() 
    buffer.close() 
    graphic = base64.b64encode(image_png) 
    graphic = graphic.decode('utf-8') 
    return graphic

def statistics_view(request):
    movies_per_year = statistics_view_movie_year()
    movies_per_genre = statistics_view_movie_genre()
    return render(request, 'statistics.html', {'movies_per_year': movies_per_year, 'movies_per_genre': movies_per_genre})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})