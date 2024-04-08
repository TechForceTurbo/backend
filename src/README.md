# Проект Чат-бот с YandexGPT для онлайн-маркетплейса vink.ru.

### Описание
Данный проект включает в себя консультирующего чат-бота на сайт vink.ru, а также бота для телеграма. За логику ответов отвечает языковая модель от YandexGPT, которая была предварительно дообучена специально под данный проект. Бот умеет отвечать на типовые запросы клиентов, а также переводить диалог на оператора.

### Адреса сервера, на котором запущен проект, и телеграм бота:
https://chat-bot-tft.vercel.app

https://t.me/vink_shop_bot

## Запуск:

### Локальный запуск проекта:

1. Клонируйте репозиторий:
```
git clone github.com/TechForceTurbo/backend.git
```
2. Перейдите в папку /src
3. Установите окружение и зависимости (предварительно установите poetry https://python-poetry.org/docs/#installation):
```bash
$ poetry install
```
4. Активируйте окружение:
```bash
$ poetry shell
```
5. Выполните команду:
```bash
$ python manage.py runserver
```

### Запуск на сервере (необходим Docker):

1. Скопируйте директорию /infra
2. Создайте в директории /infra файл .env со следующим содержанием:
```
API_KEY=<API_KEY>
CAT_ID=<CAT_ID>
TOKEN=<TOKEN>
```
3. Находясь в директории /infra с файлом docker-compose.yaml выполните команду:
```
sudo docker-compose up -d
```


## Стек технологий
- Python ^3.9
- Django
- Django REST Framework
- Django Channels
- Postgres
- Docker
- Aiogram
- Nginx

### Над проектом работали
**Шериф Рагимов** 

**Владислав Суворов** 