import reviews.models as models
from django.contrib import admin
from django.db.models import Avg


class GenreInLine(admin.TabularInline):
    model = models.GenreTitle
    extra = 0


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    model = models.Title
    list_display = (
        'name', 'year', 'description', 'get_rating', 'category', 'get_genres'
    )
    search_fields = (
        'name',
        'year',
        'description',
        'get_rating',
        'category__name',
        'genre__name'
    )
    empty_value_display = '-пусто-'
    inlines = [GenreInLine]

    def get_genres(self, instance):
        """Функция для вывода списка жанров произведения через запятую"""
        genres_list = instance.genre.get_queryset().order_by('?')
        return ', '.join([str(i) for i in genres_list])
    get_genres.short_description = 'Жанры'

    def get_rating(self, instance):
        """Функция для вывода списка жанров произведения через запятую"""
        return instance.reviews.all().aggregate(Avg('score'))['score__avg']
    get_rating.short_description = 'Рейтинг'


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    model = models.Review
    list_display = (
        'author', 'score', 'text', 'title', 'pub_date'
    )
    search_fields = (
        'author__username', 'title__name', 'text', 'score'
    )
    empty_value_display = '-пусто-'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    model = models.Comment
    list_display = (
        'author', 'text', 'pub_date'
    )
    search_fields = (
        'author__username', 'text'
    )
    empty_value_display = '-пусто-'


admin.site.register(models.Category)
admin.site.register(models.Genre)
