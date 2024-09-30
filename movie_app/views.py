from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review, Tag
from movie_app.serializers import (
    DirectorSerializer,
    DirectorDetailSerializer,
    MovieReviewSerializer,
    MovieDetailSerializer,
    ReviewSerializer,
    ReviewDetailSerializer,
    DirectorValidateSerializer,
    MovieValidateSerializer,
    ReviewValidateSerializer,)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from movie_app.serializers import DirectorSerializer, MovieReviewSerializer, ReviewSerializer, TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class DirectorListAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination


@api_view(['GET', 'POST'])
def director_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        name = serializer.validated_data.get('name')
        director = Director.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The director has not been found!'})
    if request.method == 'GET':
        data = DirectorDetailSerializer(director, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListAPIView(ListCreateAPIView):
    serializer_class = MovieReviewSerializer
    queryset = Movie.objects.all()
    pagination_class = PageNumberPagination


@api_view(['GET', 'POST'])
def movie_review_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieReviewSerializer(movies, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        tags = serializer.validated_data.get('tags')
        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id,
        )
        movie.tags.set(tags)
        movie.save()
        return Response(status=status.HTTP_201_CREATED, data=MovieReviewSerializer(movie).data)


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieReviewSerializer
    queryset = Movie.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The movie has not been found!'})
    if request.method == 'GET':
        data = MovieDetailSerializer(movie, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.tags.set(serializer.validated_data.get('tags'))
        movie.save()
        return Response(status=status.HTTP_201_CREATED, data=MovieReviewSerializer(movie).data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie_id')
        review = Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'Error': 'The review has not been found!'})
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
