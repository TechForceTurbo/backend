
# Чат-бот с YandexGPT для онлайн-маркетплейса Vink.ru

## Обзор
Проект представляет собой интегрированного консультационного чат-бота на сайте Vink.ru и бота для Telegram. Ответы бота генерируются языковой моделью YandexGPT, которая была дополнительно дообучена специально для этого проекта. Бот способен обрабатывать типичные запросы клиентов и, при необходимости, переводить диалог на живого оператора.


## Стек технологий
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-009688?style=for-the-badge&logo=django&logoColor=white)
![Django Channels](https://img.shields.io/badge/Django_Channels-9C27B0?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/-Postgres-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Aiogram](https://img.shields.io/badge/-Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Nginx](https://img.shields.io/badge/-Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## URL-адреса проекта и Telegram бота:
- Проект: https://chat-bot-tft.vercel.app
- Telegram Бот: https://t.me/vink_shop_bot

## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: https://docs.docker.com/get-docker/ и https://docs.docker.com/compose/install/

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:TechForceTurbo/backend.git
   cd backend/infra
   ```

2. Запустите контейнеры с помощью Docker Compose:
   ```
   docker compose -f docker-compose.local.yml up
   ```

   Теперь приложение должно быть доступно по адресу:

   http://localhost:8000
   
   А документация доступна по адресу:
   
   http://localhost:8000/api/v1/swagger/

</details>


## Над проектом работали
- [**Шериф Рагимов**](https://github.com/ragimov700)
- [**Владислав Суворов**](https://github.com/XaverD1992)