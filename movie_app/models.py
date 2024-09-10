from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Director(AbstractModel):
    pass


class Tag(AbstractModel):
    pass


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def director_name(self):
        if self.director:
            return self.director.name
        return None


STARS = (
    (i, i * '*') for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=STARS, default=5, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='reviews')

    def __str__(self):
        return self.text
