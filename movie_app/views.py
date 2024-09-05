from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET'])
def director_view(request):
    directors = Director.objects.all()
    data = DirectorSerializer(directors, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The director has not been found!'})
    data = DirectorSerializer(director, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movie_view(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The movie has not been found!'})
    data = MovieSerializer(movie, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The review has not been found!'})
    data = ReviewSerializer(review, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)
