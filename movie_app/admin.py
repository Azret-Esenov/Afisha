from django.contrib import admin
from movie_app.models import Director, Movie, Tag, Review

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Tag)
admin.site.register(Review)
