# praktikum_new_diplom

«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Доступно по:
URL - http://51.250.18.118/
login - review@review.com
pass - reviewer670821

## Инструкция по запуску проекта на удаленном сервере Ubuntu
1) Склонировать репозиторий на локальную машину:
```
git clone https://github.com/hegelianer/foodgram
```

2) Зайти на удаленный сервер, установить docker и docker-compose:
```
sudo apt install docker.io
sudo curl -L &quot;https://github.com/docker/compose/releases/download/1.29.2/docker-
compose-$(uname -s)-$(uname -m)&quot; -o /usr/local/bin/docker-compose
```

3) Cкопировать файлы docker-compose.yml и nginx.conf из директории infra
```
sudo scp docker-compose.yml &lt;username&gt;@&lt;host&gt;:/home/&lt;username&gt;/docker-compose.yml
sudo scp nginx.conf &lt;username&gt;@&lt;host&gt;:/home/&lt;username&gt;/nginx.conf
```

В nginx.conf добавить адрес Вашего сервера.

4) Cоздать и отредактировать файл .env
```
sudo touch .env
sudo nano .env
```

    В .env указать:
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=lavigne
    DB_HOST=db
    DB_PORT=5432
    DJANGO_SECRET_KEY=&lt;ваш_django_секретный_ключ&gt;

5) Собрать контейнеры:
```
sudo docker-compose up -d --build
```
    Проект запуститься в четырёх контейнерах:
        nginx:1.19.3
        postgres:12.4
        foodgram_backend
        foodgram_frontend

6) Применить миграцию, собрать статику и создать суперпользователя:
```
sudo docker-compose exec backend python manage.py collectstatic --noinput
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
```

Проект будет доступен по IP сервера

## Основные технологии
```
Python
Django
PostgreSQL
Docker
NGINX
GitHub
```

## Автор
Артём Васильев
(https://github.com/hegelianer)

hegelianer@gmail.com

## Лицензия
Проект находится под лицензией MIT см.: [LICENSE.md](LICENSE.md)

## Благодарности
Спасибо кураторам, наставникам и рецензентам Яндекс Практикума. Кажется, им тоже было
нелегко) спасибо и коллегам-студентам за неизменно ободряющие дискуссии в слэке.