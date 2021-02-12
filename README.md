1. Добавляем исходный код фреймворка GbFramework в PYTHONPATH
   https://clck.ru/TFwup

2. Устанавливаем uwsgi

3. Команда запуска локального web сервера
   uwsgi --http :8000 --wsgi-file main.py

Ссылка на репозиторий:
https://clck.ru/TFwwr

===

В проекте реализованы паттерны:
PageController
FrontController

Доступные URL:
http://localhost:8000/
http://localhost:8000/secret/

Файлы шаблоны с использованием bootstrap расположены в директории templates/:
index.html
secret.html