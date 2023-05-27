import csv
from datetime import datetime
from pathlib import Path

import reviews.models as model
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / 'static/data/'


def import_from_csv(filename, datamodel, import_func=None):
    print(f'Импортируем данные из файла {filename}')
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            if import_func:
                import_func(row, datamodel)
            else:
                line = datamodel(
                    **row
                )
                line.save()


def title_import_func(row, datamodel):
    category = model.Category.objects.filter(id=row['category'])[0]
    line = datamodel(
        id=row['id'],
        name=row['name'],
        year=row['year'],
        category=category
    )
    line.save()


def genre_title_import_func(row, datamodel):
    title = model.Title.objects.filter(id=row['title_id'])[0]
    genre = model.Genre.objects.filter(id=row['genre_id'])[0]
    line = datamodel(
        id=row['id'],
        title=title,
        genre=genre
    )
    line.save()


def review_import_func(row, datamodel):
    title = model.Title.objects.filter(id=row['title_id'])[0]
    author = User.objects.filter(id=row['author'])[0]
    time = datetime.fromisoformat(row['pub_date'][:-1])
    line = datamodel(
        id=row['id'],
        author=author,
        title=title,
        text=row['text'],
        score=row['score'],
        pub_date=time
    )
    line.save()


def comment_import_func(row, datamodel):
    review = model.Review.objects.filter(id=row['review_id'])[0]
    author = User.objects.filter(id=row['author'])[0]
    time = datetime.fromisoformat(row['pub_date'][:-1])
    line = datamodel(
        id=row['id'],
        author=author,
        review=review,
        text=row['text'],
        pub_date=time
    )
    line.save()


class Command(BaseCommand):
    help = 'Import data from static/data/ folder to DB'

    def handle(self, *args, **options):
        import_from_csv(DATA_DIR / 'users.csv', User)
        import_from_csv(DATA_DIR / 'category.csv', model.Category)
        import_from_csv(DATA_DIR / 'genre.csv', model.Genre)
        import_from_csv(
            DATA_DIR / 'titles.csv', model.Title, title_import_func
        )
        import_from_csv(
            DATA_DIR / 'genre_title.csv',
            model.GenreTitle,
            genre_title_import_func
        )
        import_from_csv(
            DATA_DIR / 'review.csv', model.Review, review_import_func
        )
        import_from_csv(
            DATA_DIR / 'comments.csv', model.Comment, comment_import_func
        )
