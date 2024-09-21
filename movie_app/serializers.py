from rest_framework import serializers
from movie_app.models import Director, Movie, Tag, Review
from rest_framework.exceptions import ValidationError


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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120)


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


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except:
            raise ValidationError('Movie does not exist.')
        return movie_id


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


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField()
    duration = serializers.FloatField(min_value=1, max_value=10000)
    director_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist.')
        return director_id

    def validate_tags(self, tags):
        tags_from_db = Tag.objects.filter(id__in=tags)
        if len(tags_from_db) != len(tags):
            raise ValidationError('Invalid tags.')
        return tags
