from rest_framework import serializers
from movie_app.models import Director, Movie, Tag, Review


class DirectorSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies'.split()

    def get_movies(self, director):
        return director.movies.count()


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()
    director = DirectorSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id title description duration director tags reviews rating'.split()

    def get_rating(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average = sum_reviews / len(reviews)
            return round(average, 1)
        return None


class MovieDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director_name created updated tags reviews'.split()
        depth = 1

    def get_tags(self, movie):
        return [tag.name for tag in movie.tags.all()]

