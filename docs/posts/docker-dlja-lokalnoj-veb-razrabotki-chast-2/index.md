---
title: 'Docker для локальной веб-разработки - часть 2'
description: 'Разбираемся, как уменьшить размер Docker-образов.'
slug: docker-dlja-lokalnoj-veb-razrabotki-chast-2
date: 2022-04-09
tags:
  - Docker
---

Всем привет! Эта статья продолжает серию переводов замечательных статей об использовании Docker для локальной веб-разработки.

<!-- more -->

## В этой серии

- [Введение: почему это должно вас волновать?](../docker-dlja-lokalnoj-veb-razrabotki-vvedenie/index.md)
- [Часть 1: базовый стек LEMP](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md)
- Часть 2: посадите свои образы на диету ⬅️ вы здесь
- [Часть 3: трёхуровневая архитектура с фреймворками](../docker-dlja-lokalnoj-veb-razrabotki-chast-3/index.md)
- [Часть 4: сглаживание ситуации с помощью Bash](../docker-dlja-lokalnoj-veb-razrabotki-chast-4/index.md)
- [Часть 5: HTTPS для всего](../docker-dlja-lokalnoj-veb-razrabotki-chast-5/index.md)
- [Часть 6: открываем локальный контейнер для доступа в Интернет](../docker-dlja-lokalnoj-veb-razrabotki-chast-6/index.md)
- [Часть 7: использование многоэтапной сборки для внедрения воркера](../docker-dlja-lokalnoj-veb-razrabotki-chast-7/index.md)
- [Часть 8: запланированные задачи](../docker-dlja-lokalnoj-veb-razrabotki-chast-8/index.md)
- [Заключение: куда идти дальше](../docker-dlja-lokalnoj-veb-razrabotki-zaklyuchenie/index.md)

## Начало работы

Предполагаемая отправная точка этого руководства находится там, где мы остановились в конце [предыдущей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md), что соответствует ветке [part-1](https://github.com/osteel/docker-tutorial/tree/part-1) репозитория.

Если вы предпочитаете, вы также можете напрямую перейти к ветке [part-2](https://github.com/osteel/docker-tutorial/tree/part-2), которая является конечным результатом сегодняшней статьи.

## «Я не толстый, я крупнокостный»

В [первой части](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md) этой серии статей мы рассмотрели шаги по созданию простого, но функционального стека LEMP, работающего на Docker и оркестрованного с помощью Docker Compose, в результате чего четыре контейнера работают одновременно.

Эти контейнеры основаны на образах, загруженных с Docker Hub, причем каждый из этих образов имеет свой вес. Но о каком объеме пространства идет речь?

Давайте выясним это с помощью простой команды, которая будет запущена из корня нашего проекта:

```bash
$ docker compose images
```

Она отобразит таблицу, содержащую образы, используемые приложением, и некоторую информацию о них, включая их вес:

```bash
Container                       Repository              Tag                 Image Id            Size
learning_project-mysql-1        mysql/mysql-server      8.0                 434c35b82b08        417MB
learning_project-nginx-1        nginx                   1.21                12766a6745ee        142MB
learning_project-php-1          learning_project_php    latest              24d89b230006        449MB
learning_project-phpmyadmin-1   phpmyadmin/phpmyadmin   5                   5682e7556577        524MB
```

Общая сумма составляет примерно 1,5 ГБ, что совсем не мало. Почему так?

Большинство дистрибутивов Linux поставляются с множеством сервисов, которые должны покрывать общие случаи использования; они предлагают большое количество программ, предназначенных для широкой аудитории, чьи потребности могут меняться со временем. С другой стороны, контейнеры Docker предназначены для запуска одного процесса, а значит, то, что им нужно для выполнения своей работы, обычно не так много, и вряд ли изменится со временем.

Используя стандартные дистрибутивы Linux, мы внедряем множество инструментов и служб, которые нам не всегда нужны, неоправданно увеличивая при этом размер образов. В свою очередь, это влияет на производительность, безопасность и, иногда, на стоимость развёртывания.

Можем ли мы что-нибудь с этим поделать?

## Alpine Linux

[Alpine](https://alpinelinux.org/) — это дистрибутив Linux, который использует противоположный подход: ориентированный на безопасность и занимающий небольшую площадь, он по умолчанию включает в себя самый минимум и позволяет устанавливать то, что действительно необходимо для вашего приложения. Докеризованная версия Alpine занимает всего 4 МБ, и большинство официальных образов Docker содержат версию, основанную на этом дистрибутиве.

Прежде чем изменять нашу установку, давайте избавимся от текущей:

```bash
$ docker compose down -v --rmi all --remove-orphans
```

Эта команда остановит и/или уничтожит контейнеры, а также удалит тома и образы, что позволит нам начать всё заново.

Замените содержимое `docker-compose.yml` на это:

```yaml
version: '3.8'

# Services
services:
  # Nginx Service
  nginx:
    image: nginx:1.21-alpine
    ports:
      - 80:80
    volumes:
      - ./src:/var/www/php
      - ./.docker/nginx/conf.d:/etc/nginx/conf.d
      - phpmyadmindata:/var/www/phpmyadmin
    depends_on:
      - php
      - phpmyadmin

  # PHP Service
  php:
    build: ./.docker/php
    working_dir: /var/www/php
    volumes:
      - ./src:/var/www/php
    depends_on:
      mysql:
        condition: service_healthy

  # MySQL Service
  mysql:
    image: mysql/mysql-server:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_ROOT_HOST: '%'
      MYSQL_DATABASE: demo
    volumes:
      - ./.docker/mysql/my.cnf:/etc/mysql/conf.d/my.cnf
      - mysqldata:/var/lib/mysql
    healthcheck:
      test: mysqladmin ping -h 127.0.0.1 -u root --password=$$MYSQL_ROOT_PASSWORD
      interval: 5s
      retries: 10

  # PhpMyAdmin Service
  phpmyadmin:
    image: phpmyadmin/phpmyadmin:5-fpm-alpine
    environment:
      PMA_HOST: mysql
    volumes:
      - phpmyadmindata:/var/www/html
    depends_on:
      mysql:
        condition: service_healthy

# Volumes
volumes:
  mysqldata:

  phpmyadmindata:
```

Давайте разберем это по порядку. Для Nginx мы просто добавили `-alpine` к тегу image, чтобы получить версию на базе Alpine (помните, что доступные версии образа перечислены на [Docker Hub](https://hub.docker.com/_/nginx)). Мы также смонтировали новый именованный том `phpmyadmindata` (объявленный в нижней части файла) и использовали `depends_on`, чтобы указать, что контейнер phpMyAdmin должен быть запущен первым.

Причина в том, что теперь Nginx будет обслуживать phpMyAdmin, а также наше PHP-приложение, тогда как раньше образ phpMyAdmin обслуживал собственный HTTP-сервер (Apache). Как следует из названия, тег `5-fpm-alpine` - это Alpine-версия образа, контейнер которой запускает PHP-FPM как процесс и ожидает, что PHP-файлы будут обрабатываться внешним HTTP-сервером.

!!! note "Примечание"

    Где искать информацию?

    Использование внешнего HTTP-сервера для phpMyAdmin фактически не документировано, и мне пришлось раскопать какой-то [вопрос на GitHub](https://github.com/phpmyadmin/docker/issues/253), чтобы встать на правильный путь. Это хороший пример того, где искать информацию, когда официальной документации недостаточно: просмотр проблем на GitHub обычно является хорошим местом для начала, поскольку кто-то, вероятно, уже сталкивался с такой же проблемой. Иногда также полезно взглянуть на `Dockerfile` образа, поскольку проще использовать образ, когда мы понимаем, как он собран.

Теперь нам нужна конфигурация Nginx для phpMyAdmin. Давайте создадим новый файл `phpmyadmin.conf` в `.docker/nginx/conf.d`, рядом с `php.conf`:

```nginx
server {
    listen      80;
    listen      [::]:80;
    server_name phpmyadmin.test;
    root        /var/www/phpmyadmin;
    index       index.php;

    location ~* \.php$ {
        fastcgi_pass   phpmyadmin:9000;
        root           /var/www/html;
        include        fastcgi_params;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param  SCRIPT_NAME     $fastcgi_script_name;
    }
}
```

Опять же, довольно стандартная конфигурация сервера, которая очень похожа на `php.conf`, за исключением того, что она указывает на порт 9000 службы phpMyAdmin.

Вам также нужно обновить локальный файл `hosts`, чтобы добавить новое доменное имя (посмотрите [здесь](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md#domennoe-imia), если вы забыли, как это сделать):

```
127.0.0.1 php.test phpmyadmin.test
```

Вернемся к `docker-compose.yml`: аналогично нашему PHP-приложению, том `phpmyadmindata` обеспечивает доступность файлов phpMyAdmin для Nginx, с той лишь разницей, что вместо монтирования локальной папки по нашему выбору (например, `src`), мы позволили Docker Compose выбрать локальную папку для монтирования контейнеров Nginx и phpMyAdmin, эффективно делая содержимое последнего доступным для первого.

Наконец, мы также избавились от привязки порта 8080, поскольку теперь мы будем использовать порт 80 непосредственно для Nginx.

Далее на очереди — PHP. Если вы следили за [предыдущей частью](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md), вы уже знаете, что для описания и сборки нашего образа мы используем `Dockerfile`, расположенный в `.docker/php`.

Замените его содержимое на это:

```docker
FROM php:8.1-fpm-alpine

RUN docker-php-ext-install pdo_mysql
```

Как и в случае с Nginx, единственное отличие заключается в том, что мы добавили `-alpine` в конце тега образа, чтобы получить версию, основанную на Alpine.

Остается сервис MySQL, который не претерпел никаких изменений. Причина в том, что на момент написания статьи для образа MySQL просто нет доступной версии Alpine, по причинам, изложенным в этом [вопросе GitHub](https://github.com/docker-library/mysql/issues/179).

!!! note "Примечание"

    Примечание переводчика: всегда можно заменить MySQL на альтернативный образ на базе MariaDB, например, [yobasystems/alpine-mariadb](https://hub.docker.com/r/yobasystems/alpine-mariadb), имеющий в два раза меньший объём. Кроме того, на phpMyAdmin тоже свет клином не сошёлся, и есть прекрасная альтернатива в виде [Adminer](https://hub.docker.com/_/adminer).

Теперь мы готовы протестировать нашу новую установку. Снова запустите ставшую уже привычной команду `docker compose up -d`, а затем `docker compose images`:

```bash
Container                       Repository              Tag                 Image Id            Size
learning_project-mysql-1        mysql/mysql-server      8.0                 434c35b82b08        417MB
learning_project-nginx-1        nginx                   1.21-alpine         51696c87e77e        23.4MB
learning_project-php-1          learning_project_php    latest              198fa3140e01        73.4MB
learning_project-phpmyadmin-1   phpmyadmin/phpmyadmin   5-fpm-alpine        d501a2531c80        145MB
```

Общий размер наших образов теперь составляет около 650 МБ, что меньше половины первоначального веса.

И, в качестве бонуса, теперь вы можете получить доступ к phpMyAdmin по адресу [phpmyadmin.test](http://phpmyadmin.test/), вместо _localhost:8080_.

## Когда не стоит использовать Alpine

Однако, как часто бывает, серебряной пули не существует. Alpine хорош до тех пор, пока всё, что вам нужно, доступно из официального [репозитория пакетов](https://pkgs.alpinelinux.org/packages), но если чего-то не хватает, вам придется [повозиться](https://dev.to/asyazwan/moving-away-from-alpine-30n4), чтобы добавить это вручную. Если вы не разбираетесь в системном администрировании, вам, вероятно, не стоит туда лезть.

Как же выбрать правильную версию образа? Хорошим подходом будет начать с самой минимальной доступной версии и двигаться вверх по лестнице версий только при отсутствия поддержки нужных зависимостей. Хотя ничто не вечно, и вы всегда можете изменить базовый образ позже, чем сложнее `Dockerfile`, тем более болезненным может оказаться его перенос на другой дистрибутив Linux.

Вот почему я представляю Alpine так рано: вместо того, чтобы без раздумий брать первый попавшийся образ, рассмотрите свои возможности и определите, что кажется лучшим компромиссом — это, скорее всего, избавит вас от головной боли в дальнейшем.

Помните также, что чем меньше образ, тем меньше потенциальная [поверхность атаки](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B2%D0%B5%D1%80%D1%85%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%B0%D1%82%D0%B0%D0%BA%D0%B8).

## Заключение

Теперь мы лучше представляем, как выбрать базовый образ для наших контейнеров, и в результате оптимизировали наш стек LEMP. Это хорошее место для того, чтобы модернизировать нашу установку до более сложной трехуровневой архитектуры и внедрить фреймворки приложений, о которых мы расскажем в [следующей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-3/index.md).

---

Оригинальная статья: [Docker for local web development, part 2: put your images on a diet](https://tech.osteel.me/posts/docker-for-local-web-development-part-2-put-your-images-on-a-diet) (English)
