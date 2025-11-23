---
title: 'Docker для локальной веб-разработки - часть 7'
description: 'Экономим время, ресурсы и нервы с помощью этапов в Docker-файлах.'
slug: docker-dlja-lokalnoj-veb-razrabotki-chast-7
date: 2022-04-24
tags:
  - Docker
---

Всем привет! Эта статья продолжает серию переводов замечательных статей об использовании Docker для локальной веб-разработки.

<!-- more -->

## В этой серии

- [Введение: почему это должно вас волновать?](../docker-dlja-lokalnoj-veb-razrabotki-vvedenie/index.md)
- [Часть 1: базовый стек LEMP](../docker-dlja-lokalnoj-veb-razrabotki-chast-1/index.md)
- [Часть 2: посадите свои образы на диету](../docker-dlja-lokalnoj-veb-razrabotki-chast-2/index.md)
- [Часть 3: трёхуровневая архитектура с фреймворками](../docker-dlja-lokalnoj-veb-razrabotki-chast-3/index.md)
- [Часть 4: сглаживание ситуации с помощью Bash](../docker-dlja-lokalnoj-veb-razrabotki-chast-4/index.md)
- [Часть 5: HTTPS для всего](../docker-dlja-lokalnoj-veb-razrabotki-chast-5/index.md)
- [Часть 6: открываем локальный контейнер для доступа в Интернет](../docker-dlja-lokalnoj-veb-razrabotki-chast-6/index.md)
- Часть 7: использование многоэтапной сборки для внедрения воркера ⬅️ вы здесь
- [Часть 8: запланированные задачи](../docker-dlja-lokalnoj-veb-razrabotki-chast-8/index.md)
- [Заключение: куда идти дальше](../docker-dlja-lokalnoj-veb-razrabotki-zaklyuchenie/index.md)

## Введение

Никому не нравятся медленные сайты.

Страницы с большим временем отклика имеют более высокий показатель отказов, что приводит к снижению конверсии. Если ваш сайт зависит от API, вы хотите, чтобы API работал быстро — вы не хотите чувствовать себя так, будто он выпивает чашку чая с вашим запросом, а затем настаивает на том, чтобы в ответе была ещё одна булочка с маслом, прежде чем отправить его вам.

Существует множество способов повысить отзывчивость API, и один из них, о котором пойдет речь в сегодняшней статье, — это использование очередей. Очереди — это, по сути, списки задач, которые, в отличие от чистки зубов зубной нитью, в конечном итоге будут выполнены. Что важно в этих задачах — называемых заданиями — так это то, что их не нужно выполнять в течение жизненного цикла первоначального запроса.

Типичные примеры таких заданий включают отправку приветственного письма, изменение размера изображения или подсчет статистики — какой бы ни была задача, нет необходимости заставлять конечного пользователя ждать её выполнения. Вместо этого задание помещается в очередь, чтобы быть рассмотренным позже, а ответ немедленно отправляется клиенту. Другими словами, задание становится асинхронным, что позволяет значительно ускорить время отклика.

Задания, стоящие в очереди, обрабатываются так называемыми воркерами (рабочими). Воркеры следят за очередями и принимают задания по мере их появления — они немного похожи на кассиров в супермаркете, обрабатывающих содержимое тележек по мере их поступления. И точно так же, как при внезапном наплыве покупателей можно вызвать на подмогу дополнительных кассиров, можно добавить дополнительных работников, если очереди заполняются быстрее, чем освобождаются.

Наконец, очереди — это, по сути, списки сообщений, которые необходимо хранить в базе данных, которую иногда называют _брокером сообщений_. [Redis](https://redis.io/) — отличный выбор для этого, поскольку он очень быстрый (хранение в памяти) и предлагает структуры данных, хорошо подходящие для такого рода вещей. Его также очень легко установить с помощью Docker и он отлично сочетается с Laravel, поэтому сегодня мы будем использовать именно его.

Предполагаемая отправная точка этого руководства находится там, где мы остановились в конце [предыдущей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-6/index.md), что соответствует [ветке part-6](https://github.com/osteel/docker-tutorial/tree/part-6) репозитория.

Если вы предпочитаете, вы также можете напрямую перейти к [ветке part-7](https://github.com/osteel/docker-tutorial/tree/part-7), которая является конечным результатом этой статьи.

## Установка Redis

Теперь, когда все персонажи представлены, пора приступить к сюжету.

Первое, что нам нужно сделать, это установить расширение Redis для PHP, поскольку оно не входит в состав предварительно скомпилированных. Поскольку это расширение немного сложно в установке, мы воспользуемся [удобным скриптом](https://github.com/mlocati/docker-php-extension-installer), представленным в [официальной документации по образам PHP](https://hub.docker.com/_/php), который упрощает установку расширений PHP для всех дистрибутивов Linux.

Замените содержимое Dockerfile бэкенда на этот:

```docker
FROM php:8.1-fpm-alpine

# Import extension installer
COPY --from=mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/bin/

# Install extensions
RUN install-php-extensions pdo_mysql bcmath opcache redis

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

# Configure PHP
COPY .docker/php.ini $PHP_INI_DIR/conf.d/opcache.ini

# Use the default development configuration
RUN mv $PHP_INI_DIR/php.ini-development $PHP_INI_DIR/php.in

# Install extra packages
RUN apk --no-cache add bash mysql-client mariadb-connector-c-dev

# Create user based on provided user ID
ARG HOST_UID
RUN adduser --disabled-password --gecos "" --uid $HOST_UID demo

# Switch to that user
USER demo
```

Обратите внимание, что `redis` был добавлен в список расширений.

Соберём образ:

```bash
$ demo build backend
```

Наша следующая задача — запустить экземпляр Redis. В соответствии с принципом запуска одного процесса на контейнер, мы создадим выделенный сервис в `docker-compose.yml`, и поскольку [официальные образы](https://hub.docker.com/_/redis) включают версию Alpine, мы будем использовать именно её:

```yaml
# Redis Service
redis:
  image: redis:6-alpine
  command: ['redis-server', '--appendonly', 'yes']
  volumes:
    - redisdata:/data
```

[Команда запуска](https://github.com/docker-library/redis/blob/master/6.0/Dockerfile) образа по умолчанию — `redis-server` без опции, но, [согласно документации](https://hub.docker.com/_/redis), она не включает сохранение данных. Чтобы включить его, нам нужно установить опцию `appendonly` в `yes` в секции `command`, отменяя значение по умолчанию (здесь также показано, как сделать это без использования Dockerfile).

Чтобы персистентность данных была полностью функциональной, нам также нужен том, который будет добавлен в нижней части файла:

```yaml
# Volumes
volumes:
  mysqldata:

  phpmyadmindata:

  redisdata:
```

Наконец, поскольку сервис Redis будет использоваться сервисом `backend`, нам нужно убедиться, что первый запущен раньше второго. Обновите конфигурацию:

```yaml
# Backend Service
backend:
  build:
    context: ./src/backend
    args:
      HOST_UID: $HOST_UID
  working_dir: /var/www/backend
  volumes:
    - ./src/backend:/var/www/backend
    - ./.docker/backend/init:/opt/files/init
    - ./.docker/nginx/certs:/usr/local/share/ca-certificates
  depends_on:
    mysql:
      condition: service_healthy
    redis:
      condition: service_started
```

Сохраните `docker-compose.yml` и запустите проект, чтобы загрузить новый образ и создать соответствующий контейнер и том:

```bash
$ demo start
```

Это также воссоздаст контейнер бэкенда, чтобы использовать обновленный образ, который мы создали ранее — тот, который включает расширение Redis.

Чтобы убедиться, что Redis работает правильно, посмотрите в логи:

```bash
$ demo logs redis
```

Перед созданием задания нам нужно сделать ещё одну вещь: бэкенд-приложение настроено на немедленный запуск заданий, а нам нужно указать ему, чтобы оно ставило их в очередь, используя Redis.

Откройте `src/backend/.env` и найдите следующую строку:

```ini
QUEUE_CONNECTION=sync
```

Замените её на эти две строки:

```ini
QUEUE_CONNECTION=redis
REDIS_HOST=redis
```

Это всё, что нам нужно, потому что значения по умолчанию других параметров уже являются правильными (вы можете найти их в `src/backend/config/database.php`).

!!! note "Примечание"

    Мониторинг Redis

    Если вы хотите использовать внешний инструмент для доступа к базе данных Redis, вы можете просто обновить конфигурацию сервиса в `docker-compose.yml` и добавить секцию `ports`, сопоставляющую порт 6379 вашей локальной машины с портом контейнера:

    ```
        ...
          порты:
            - 6379:6379
        ...
    ```

    После этого всё, что вам нужно сделать, это настроить подключение к базе данных в выбранном вами программном обеспечении, указав `localhost:6379` для доступа к базе данных Redis во время работы контейнера.

    Как отметил [Уткарш Вишной](http://disq.us/p/29sa81j), вы также можете настроить новый сервис для запуска [Redis Commander](https://hub.docker.com/r/rediscommander/redis-commander), немного похожий на то, что мы сделали с phpMyAdmin.

## Задание

Laravel имеет встроенные инструменты, которые мы можем использовать для создания задания:

```bash
$ demo artisan make:job Time
```

Эта команда создаст новую папку `Jobs` в `src/backend/app`, содержащую файл `Time.php`. Откройте его и измените содержимое метода `handle` на это:

```php
<?php // ignore this line, it's for syntax highlighting only

/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    \Log::info(sprintf('It is %s', date('g:i a T')));
}
```

Всё, что делает задание, это регистрирует текущее время. Класс уже обладает всеми необходимыми свойствами, чтобы сделать его _пригодным для постановки в очередь_, поэтому нет необходимости беспокоиться об этом.

Laravel имеет [хороший планировщик команд](https://laravel.com/docs/scheduling), который мы можем использовать для определения заданий, которые должны выполняться периодически, со [встроенными помощниками](https://laravel.com/docs/scheduling#scheduling-queued-jobs) для управления заданиями в очереди.

Откройте файл `src/backend/app/Console/Kernel.php` и обновите метод `schedule`:

```php
<?php // ignore this line, it's for syntax highlighting only

/**
 * Define the application's command schedule.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->job(new \App\Jobs\Time)->everyMinute();
}
```

По сути, мы просим планировщик отправлять задание `Time` каждую минуту.

Однако сам он этого делать не будет, его нужно запустить с помощью команды Artisan. Но прежде чем мы запустим его, мы запустим воркера очереди вручную, чтобы видеть, как задания обрабатываются в реальном времени.

Откройте новое окно терминала и выполните следующую команду:

```bash
$ demo artisan queue:work
```

Теперь вы можете вернуться в первое окно терминала и запустить планировщик:

```bash
$ demo artisan schedule:run
```

И если вы теперь откроете `src/backend/storage/logs/laravel.log`, вы увидите новую строку, которая была создана этим заданием.

Наша очередь запущена! Теперь вы можете закрыть окно терминала воркера, что также приведет к его остановке.

Однако это был всего лишь тест. Мы не хотим вручную запускать воркера в отдельном окне каждый раз при запуске проекта — нам нужно, чтобы это происходило автоматически.

## Правильный воркер

Здесь мы наконец-то используем [многоступенчатую сборку](https://docs.docker.com/develop/develop-images/multistage-build/). Идея заключается в том, чтобы разделить Dockerfile на различные секции, содержащие немного разные конфигурации, которые могут быть направлены по отдельности для создания различных образов. Давайте посмотрим, что это значит на практике.

Замените содержимое `src/backend/Dockerfile` на это:

```docker
FROM php:8.1-fpm-alpine as backend

# Import extension installer
COPY --from=mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/bin/

# Install extensions
RUN install-php-extensions bcmath pdo_mysql opcache redis

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

# Configure PHP
COPY .docker/php.ini $PHP_INI_DIR/conf.d/opcache.ini

# Use the default development configuration
RUN mv $PHP_INI_DIR/php.ini-development $PHP_INI_DIR/php.ini

# Install extra packages
RUN apk --no-cache add bash mysql-client mariadb-connector-c-dev

# Create user based on provided user ID
ARG HOST_UID
RUN adduser --disabled-password --gecos "" --uid $HOST_UID demo

# Switch to that user
USER demo


FROM backend as worker

# Start worker
CMD ["php", "/var/www/backend/artisan", "queue:work"]
```

Теперь у нас есть два отдельных этапа: `backend` и `worker`. Первый — это, по сути, исходный Dockerfile — мы просто назвали его `backend`, используя ключевое слово `as` в самом верху:

```docker
FROM php:8.1-fpm-alpine as backend
```

Второй предназначен для описания воркера и основан на первом:

```docker
FROM backend as worker

# Start worker
CMD ["php", "/var/www/backend/artisan", "queue:work"]
```

Всё, что мы делаем здесь, это повторно используем стадию `backend` почти как есть, только переопределяем её команду по умолчанию, определяя вместо нее команду `queue:work Artisan`. Другими словами, всякий раз, когда запускается контейнер для стадии `worker`, его запущенный процесс будет по умолчанию рабочим процессом очереди, а не PHP-FPM.

Как запустить такой контейнер? Сначала нам нужно определить отдельный сервис в `docker-compose.yml`:

```yaml
# Worker Service
worker:
  build:
    context: ./src/backend
    target: worker
    args:
      HOST_UID: $HOST_UID
  working_dir: /var/www/backend
  volumes:
    - ./src/backend:/var/www/backend
  depends_on:
    - backend
```

Всё это выглядит уже знакомо, за исключением секции `build`, которая теперь имеет дополнительное свойство: `target`. Это свойство позволяет нам указать, какой `stage` (этап) должен использоваться в качестве базового образа для контейнеров сервиса.

Мы почти закончили работу с `docker-compose.yml` — нам осталось обновить определение сервиса `backend`, чтобы указать ему целевую стадию `backend`:

```yaml
# Backend Service
backend:
  build:
    context: ./src/backend
    target: backend
    args:
      HOST_UID: $HOST_UID
  working_dir: /var/www/backend
  volumes:
    - ./src/backend:/var/www/backend
    - ./.docker/backend/init:/opt/files/init
    - ./.docker/nginx/certs:/usr/local/share/ca-certificates
  depends_on:
    mysql:
      condition: service_healthy
    redis:
      condition: service_started
```

Сохраните файл и постройте соответствующие образы:

```bash
$ demo build backend
$ demo build worker
```

Запустите проект для получения новых образов:

```bash
$ demo start
```

Затем снова запустите планировщик:

```bash
$ demo artisan schedule:run
```

Если всё прошло успешно, задание должно быть запланировано, и в логе `src/backend/storage/laravel.log` появится новая строка, а в логах контейнера `worker` появится пара новых строк:

```bash
$ demo logs worker
```

Наш воркер завершен! Он будет тихо работать в фоновом режиме каждый раз, когда вы запускаете свой проект, готовый обработать любое задание, которое поручит ему ваше приложение.

## Обновление скрипта инициализации

Если вы были со мной с самого начала и используете Bash-слой для управления настройками, всё, что осталось сделать, это обновить скрипт инициализации бэкенда, чтобы он использовал Redis для очередей по умолчанию.

Шаги очень похожи на те, что мы делали в начале этой статьи — откройте `.docker/backend/init` и исправьте следующую строку:

```ini
QUEUE_CONNECTION=sync
```

Замените её на эти две строки и сохраните файл:

```ini
QUEUE_CONNECTION=redis
REDIS_HOST=redis
```

Готово!

## Заключение

Многоэтапные сборки — это мощный инструмент, о котором мы рассказали лишь вкратце. Каждая стадия может относиться к отдельному образу, что позволяет сопровождающим придумывать всевозможные конвейерные сборки, в которых инструменты, используемые на каждой стадии, отбрасываются, чтобы сохранить только конечный результат в результирующем образе. Подумайте об этом минутку.

Я также рекомендую вам ознакомиться с [этими лучшими практиками](https://www.docker.com/blog/intro-guide-to-dockerfile-best-practices/), чтобы убедиться, что вы получаете максимальную отдачу от ваших Docker-файлов.

Redis также можно использовать не только как простой брокер сообщений. Например, вы можете использовать его в качестве локального кэш-слоя прямо сейчас, вместо того чтобы использовать `массивы` или `файловые драйверы` Laravel.

Наконец, сегодняшняя статья оставляет нас с парой замечаний: первое — жизнь слишком коротка для чистки зубов; второе — до сих пор мы запускали планировщик Laravel вручную, хотя в документации указано, что для этого следует использовать [запись cron](https://laravel.com/docs/scheduling#introduction). Как нам это исправить?

В [следующей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-8/index.md) этой серии мы представим планировщик для периодического запуска задач способом Docker, без использования традиционных заданий cron.

---

Оригинальная статья: [Docker for local web development, part 7: using a multi-stage build to introduce a worker](https://tech.osteel.me/posts/docker-for-local-web-development-part-7-using-a-multi-stage-build-to-introduce-a-worker) (English)
