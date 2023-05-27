import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre,
    GenreTitle, Review, Title
)
from users.models import User

model_csv_equal = {
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': GenreTitle,
    'static/data/users.csv': User,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """Команда для импорта csv в базу
    Вызов python3 manage.py importcsv
    из терминала в соответствующей папке
    """

    help = 'Импорт csv файлов в таблицы базы'

    def handle(self, *args, **options):

        with open(User, 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

        with open(Category, 'r',
                  encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Category.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug']
                )

        with open(Genre, 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Genre.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug']
                )

        with open(Title, 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Title.objects.get_or_create(
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )

        with open(GenreTitle) as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                GenreTitle.title = GenreTitle.objects.get(id=row['title_id'])
                GenreTitle.genre = GenreTitle.objects.get(id=row['genre_id'])

        with open(Review, 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )

        with open(Comment, 'r',
                  encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Comment.objects.get_or_create(
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно загружена.'))
