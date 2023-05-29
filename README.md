# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Стек технологий использованный в проекте:
-   Python
-   Django
-   Django REST Framework
-   REST API
-   SQLite
-   Аутентификация по JWT-токену

## Запуск проекта

http://158.160.50.235

Клонирование репозитория

![example workflow](https://github.com/anastasia-kassina/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Создайте файл .env в директории /infra для работы с базой данных. 
Заполните его по шаблону:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Поднимаем контейнеры
```
docker compose up -d --build
```
Выполнить миграции:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
Создаем суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
Собираем статику
```
docker-compose exec web python manage.py collectstatic --no-input
```