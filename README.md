# architecture-design-patterns-web
[Репозиторий кода](https://clck.ru/TFwwr)

### Как запустить проект

1. Добавляем исходный код фреймворка [GbFramework](https://clck.ru/TFwup) в PYTHONPATH
   

2. Устанавливаем uwsgi

3. Запускаем локальный web сервер
```
uwsgi --http :8000 --wsgi-file main.py
```
### Краткое описание проекта

В проекте реализованы паттерны:
- PageController
- FrontController
- Обработка параметров url get запроса
- Обработка параметров формы post запроса

Доступные URL:
- http://localhost:8000/
- http://localhost:8000/secret/
- http://localhost:8000/contact/

Файлы шаблоны с использованием bootstrap расположены в директории templates/:
- index.html
- secret.html
- contact.html