---
title: 'Laradock'
description: 'Полноценная среда разработки на PHP для Docker'
slug: laradock
date: 2024-01-30
tags:
  - Docker
  - Laradock
  - инструменты
---

_Laradock_ поддерживает множество общих сервисов, все из которых предварительно настроены для создания готовой среды разработки на PHP.

<!-- more -->

## Требования

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Введение

Настройка нескольких вариантов окружения для множества разных проектов может быть довольно утомительной. Для облегчения подобных задач и предлагается использовать [Laradock](https://github.com/laradock/laradock).

## Установка

К нашим услугам два вида установки — для одного проекта и для нескольких.

Если вам нужна отдельная среда Docker для каждого проекта, следуйте этой инструкции.

### PHP-проект уже есть

Если вы используете Git, выполните в корне проекта эту команду:

```bash
git submodule add https://github.com/Laradock/laradock.git
```

Если Git не используете, нужна другая команда:

```bash
git clone https://github.com/laradock/laradock.git
```

Убедитесь, что структура вашего проекта соответствует такой:

```
project-a
├───laradock-a
├───public
project-b
├───laradock-b
└───public
```

На этом всё, переходите к главе _Использование_.

### PHP-проекта пока нет

Создайте папку для проекта, откройте в ней консоль и выполните команду:

```bash
git clone https://github.com/laradock/laradock.git
```

Структура вашего проекта должна соответствовать следующей:

```
root
├───laradock
└───project
    └───public
```

Скопируйте файл `.env.example` под именем `.env`:

```bash
cp .env.example .env
```

Откройте скопированный файл и отредактируйте переменную `APP_CODE_PATH_HOST` так:

```ini
APP_CODE_PATH_HOST=../project-z/
```

На этом всё, переходите к главе _Использование_.

### Установка для нескольких проектов

Выполните следующие действия, если вам нужна единая среда Docker для всех ваших проектов.

```bash
git clone https://github.com/laradock/laradock.git
```

Структура вашего проекта должна соответствовать следующей:

```
root
├───laradock
├───project-1
│   └───public
└───project-2
    └───public
```

Переменная `APP_CODE_PATH_HOST` в файле `.env` должна указывать на корневой каталог:

```ini
APP_CODE_PATH_HOST=../
```

Определитесь с сервером, который будете использовать, и создайте файлы конфигурации, которые будут указывать на другой каталог проекта при посещении разных доменов:

Для Nginx перейдите в `nginx/sites`, для Apache2 — `apache2/sites`.

По умолчанию включено несколько примеров файлов, которые вы можете скопировать: `app.conf.example`, `laravel.conf.example` и `symfony.conf.example`.

Переименуйте файлы конфигурации по шаблону `*.conf`.

Вы можете переименовывать файлы конфигурации, папки проекта и домены по своему усмотрению, только убедитесь, что корень в файлах конфигурации указывает на правильное имя папки проекта.

Добавьте домены в файл `hosts`:

```ini
127.0.0.1  project-1.test
127.0.0.1  project-2.test
```

## Настройка

В файле `.env` можно изменить основные переменные, которые вам могут понадобиться. Например:

```ini
# Define the prefix of container names. This is useful if you have multiple projects that use laradock to have separate containers per project.
COMPOSE_PROJECT_NAME=laradock
```

```ini
# Accepted values: 8.3 - 8.2 - 8.1 - 8.0 - 7.4 - 7.3 - 7.2 - 7.1 - 7.0 - 5.6
PHP_VERSION=8.3
```

После изменения версии нужно пересобирать образ `php-fpm`: `docker-compose build php-fpm`.

```ini
### NGINX #################################################

NGINX_HOST_HTTP_PORT=80
NGINX_HOST_HTTPS_PORT=443
NGINX_HOST_LOG_PATH=./logs/nginx/
NGINX_SITES_PATH=./nginx/sites/
NGINX_PHP_UPSTREAM_CONTAINER=php-fpm
NGINX_PHP_UPSTREAM_PORT=9000
NGINX_SSL_PATH=./nginx/ssl/
```

```ini
### APACHE ################################################

APACHE_HOST_HTTP_PORT=80
APACHE_HOST_HTTPS_PORT=443
APACHE_HOST_LOG_PATH=./logs/apache2
APACHE_SITES_PATH=./apache2/sites
APACHE_PHP_UPSTREAM_CONTAINER=php-fpm
APACHE_PHP_UPSTREAM_PORT=9000
APACHE_PHP_UPSTREAM_TIMEOUT=60
APACHE_DOCUMENT_ROOT=/var/www/
APACHE_SSL_PATH=./apache2/ssl/
APACHE_INSTALL_HTTP2=false
APACHE_FOR_MAC_M1=false
```

```ini
### MYSQL #################################################

MYSQL_VERSION=latest
MYSQL_DATABASE=default
MYSQL_USER=default
MYSQL_PASSWORD=secret
MYSQL_PORT=3306
MYSQL_ROOT_PASSWORD=root
MYSQL_ENTRYPOINT_INITDB=./mysql/docker-entrypoint-initdb.d
```

```ini
### MARIADB ###############################################

MARIADB_VERSION=latest
MARIADB_DATABASE=default
MARIADB_USER=default
MARIADB_PASSWORD=secret
MARIADB_PORT=3306
MARIADB_ROOT_PASSWORD=root
MARIADB_ENTRYPOINT_INITDB=./mariadb/docker-entrypoint-initdb.d
```

```ini
### POSTGRES ##############################################

POSTGRES_VERSION=alpine
POSTGRES_CLIENT_VERSION=15
POSTGRES_DB=default
POSTGRES_USER=default
POSTGRES_PASSWORD=secret
POSTGRES_PORT=5432
POSTGRES_ENTRYPOINT_INITDB=./postgres/docker-entrypoint-initdb.d
```

```ini
### ADMINER ###############################################

ADM_PORT=8081
ADM_INSTALL_MSSQL=false
ADM_PLUGINS=
ADM_DESIGN=pepa-linha
ADM_DEFAULT_SERVER=mysql
```

## Использование

Осталось запустить что-то вроде `docker-compose up -d nginx mysql phpmyadmin` для установки выбранных компонентов. Не забудьте перед этим перейти в директорию `laradock` в командной строке. Процесс может быть достаточно долгим, заранее запаситесь чаем и печенюшками. Ну или что вы там больше всего любите.

!!! note "Примечание"

    Контейнеры `nginx` и `apache` зависят от контейнера `php-fpm`, поэтому при запуске любого из них нет необходимости добавлять в команду `php-fpm`, он запустится автоматически. Если же вам всё-таки _кровь из носу_ понадобится это сделать, запускайте в следующей последовательности: `docker-compose up -d nginx php-fpm mysql`.

Список всех доступных сервисов можно посмотреть в `docker-compose.yml`. А для их настройки загляниту в папку с соответствующим именем компонента внутри директории `laradock`.

Для остановки проекта используем `docker-compose down`.

## Вместо заключения

Размер всей папки Laradock сразу после установки — чуть больше 20 МБ. После настройки проекта вы одной командой (`docker-compose up -d nginx mysql adminer`) можете получить полностью сконфигурированные Nginx, MySQL и Adminer (либо любые другие зависимости, на ваш выбор). Для каждого проекта можно настроить свои варианты окружения: сервер базы данных, версию PHP и прочее. Laradock работает с помощью Docker, а значит везде, где работает Docker: в Windows, Linux, Mac OS.

Размер дистрибутива OS Panel, предлагаемый для скачивания на официальном сайте — 946 МБ. Свои варианты окружения для каждого проекта настраиваются только в 6 версии, в 5 такого нет. После каждого изменения модулей приходится перезагружать панельку. Open Server работает только в Windows.

Что вам больше нравится? Правильного ответа нет, у каждого свои вкусы и требования. [Попробуйте](https://laradock.io/docs/Intro) и сравните.
