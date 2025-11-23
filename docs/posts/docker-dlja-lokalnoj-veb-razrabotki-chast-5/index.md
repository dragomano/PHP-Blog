---
title: 'Docker для локальной веб-разработки - часть 5'
description: 'Разбираемся, как добавить SSL-сертификат в Docker.'
slug: docker-dlja-lokalnoj-veb-razrabotki-chast-5
date: 2022-04-17
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
- Часть 5: HTTPS для всего ⬅️ вы здесь
- [Часть 6: открываем локальный контейнер для доступа в Интернет](../docker-dlja-lokalnoj-veb-razrabotki-chast-6/index.md)
- [Часть 7: использование многоэтапной сборки для внедрения воркера](../docker-dlja-lokalnoj-veb-razrabotki-chast-7/index.md)
- [Часть 8: запланированные задачи](../docker-dlja-lokalnoj-veb-razrabotki-chast-8/index.md)
- [Заключение: куда идти дальше](../docker-dlja-lokalnoj-veb-razrabotki-zaklyuchenie/index.md)

## Введение

С момента своего создания компанией Netscape Communications в 1994 году защищенный протокол передачи гипертекста (HTTPS) распространялся в Интернете всё более быстрыми темпами, и сейчас на него приходится более 80% глобального трафика (по состоянию на [февраль 2020](https://letsencrypt.org/2020/02/27/one-billion-certs.html) года). Этот рост охвата был особенно сильным в последние несколько лет, катализатором которого стали такие организации, как Internet Security Research Group — та, что стоит за бесплатным центром сертификации [Let's Encrypt](https://letsencrypt.org/) — и такие компании, как Google, чей браузер Chrome с 2018 года [помечает HTTP-сайты как небезопасные](https://www.theverge.com/2018/2/8/16991254/chrome-not-secure-marked-http-encryption-ssl).

Хотя шифрование в Интернете становится всё дешевле и проще, эта эволюция почему-то не распространяется на локальные среды, где внедрение HTTPS всё ещё не так просто, как хотелось бы.

Эта статья призвана облегчить боль, показав, как сгенерировать самоподписанный сертификат SSL/TLS и как использовать его с нашей установкой на базе Docker, тем самым ещё на один шаг приближая нас к идеальной имитации продакшен-среды.

Предполагаемой отправной точкой этого руководства является место, где мы остановились в конце [предыдущей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-4/index.md), соответствующее [ветке part-4](https://github.com/osteel/docker-tutorial/tree/part-4) репозитория.

Если вы предпочитаете, вы также можете напрямую перейти к ветке [part-5](https://github.com/osteel/docker-tutorial/tree/part-5), которая является конечным результатом сегодняшней статьи.

## Генерация сертификата

Мы сгенерируем сертификат и его ключ в новой папке `certs` в `.docker/nginx` — создайте эту папку и добавьте в нее следующий файл `.gitignore`:

```
*
!.gitignore
```

Эти две строки означают, что все файлы, содержащиеся в этом каталоге, за исключением `.gitignore`, будут игнорироваться Git'ом (это более приятная версия файла `.keep`, с которым вы иногда можете столкнуться и который предназначен для версионирования пустой папки в Git'е).

Поскольку одна из целей использования Docker — максимально избежать загромождения локальной машины, мы будем использовать контейнер для установки OpenSSL и генерации сертификата. Nginx является логичным выбором для этого — будучи нашим прокси, он будет принимать зашифрованный трафик на порт 443, а затем перенаправлять его в нужный контейнер:

![](docker_containers.jpg)

Для этого нам нужен Dockerfile, который мы добавим в директорию `.docker/nginx`:

```docker
FROM nginx:1.21-alpine

# Install packages
RUN apk --update --no-cache add openssl
```

Нам также необходимо обновить `docker-compose.yml` для ссылки на этот Dockerfile и смонтировать папку `certs` в контейнер Nginx, чтобы сделать сертификат доступным для веб-сервера. Кроме того, поскольку трафик SSL/TLS использует порт 443, порт 443 локальной машины должен быть сопоставлен с портом контейнера:

```yaml
# Nginx Service
nginx:
  build: ./.docker/nginx
  ports:
    - 80:80
    - 443:443
  volumes:
    - ./src/backend:/var/www/backend
    - ./.docker/nginx/conf.d:/etc/nginx/conf.d
    - phpmyadmindata:/var/www/phpmyadmin
    - ./.docker/nginx/certs:/etc/nginx/certs
  depends_on:
    - backend
    - frontend
    - phpmyadmin
```

Соберём новый образ:

```bash
$ demo build nginx
```

Все инструменты, необходимые для генерации нашего сертификата, теперь на месте — нам нужно только добавить соответствующую команду и функцию Bash.

Сначала обновим меню нашего приложения, расположенное в нижней части файла `demo`:

```bash
Command line interface for the Docker-based web development environment demo.

Usage:
    demo  [options] [arguments]

Available commands:
    artisan ................................... Run an Artisan command
    build [image] ............................. Build all of the images or the specified one
    cert ...................................... Certificate management commands
        generate .............................. Generate a new certificate
        install ............................... Install the certificate
    composer .................................. Run a Composer command
    destroy ................................... Remove the entire Docker environment
    down [-v] ................................. Stop and destroy all containers
                                                Options:
                                                    -v .................... Destroy the volumes as well
    init ...................................... Initialise the Docker environment and the application
    logs [container] .......................... Display and tail the logs of all containers or the specified one's
    restart [container] ....................... Restart all containers or the specified one
    start ..................................... Start the containers
    stop ...................................... Stop the containers
    update .................................... Update the Docker environment
    yarn ...................................... Run a Yarn command
```

Чтобы сэкономить нам время позже, я также добавил меню для установки сертификата, даже если мы пока не будем его реализовывать.

Добавьте соответствующие случаи в переключатель:

```bash
    cert)
        case "$2" in
            generate)
                cert_generate
                ;;
            install)
                cert_install
                ;;
            *)
                cat << EOF

Certificate management commands.

Usage:
    demo cert <command>

Available commands:
    generate .................................. Generate a new certificate
    install ................................... Install the certificate

EOF
                ;;
        esac
        ;;
```

Поскольку существует несколько подкоманд для `cert`, я также добавил подменю с их описанием. Сохраните файл и посмотрите, как выглядят новые меню:

```bash
$ demo
$ demo cert
```

Добавьте функцию `cert_generate` в файл `demo`:

```
# Generate a wildcard certificate
cert_generate () {
    rm -Rf .docker/nginx/certs/demo.test.*
    docker compose run --rm nginx sh -c "cd /etc/nginx/certs && touch openssl.cnf && cat /etc/ssl1.1/openssl.cnf > openssl.cnf && echo \"\" >> openssl.cnf && echo \"[ SAN ]\" >> openssl.cnf && echo \"subjectAltName=DNS.1:demo.test,DNS.2:*.demo.test\" >> openssl.cnf && openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout demo.test.key -out demo.test.crt -days 3650 -subj \"/CN=*.demo.test\" -config openssl.cnf -extensions SAN && rm openssl.cnf"
}
```

Первая строка функции просто избавляется от ранее созданных сертификатов и ключей, которые всё ещё могут находиться в каталоге `certs`. Вторая строка довольно длинная и немного сложная, но по сути она создает новый, одноразовый контейнер на основе образа Nginx (`docker compose run --rm nginx`) и запускает на нем кучу команд (это часть между двойными кавычками, после `sh -c`).

Я не буду вдаваться в подробности, но суть в том, что они создают самоподписанный сертификат для `*.demo.test`, а также соответствующий ключ. Самоподписанный сертификат — это сертификат, не подписанный центром сертификации; на практике вы не будете использовать такой сертификат в продакшене, но для локальной установки он вполне подойдет.

Попробуйте выполнить команду:

```bash
$ demo cert generate
```

Полученные файлы создаются в папке `/etc/nginx/certs` контейнера, которая, согласно `docker-compose.yml`, соответствует нашему локальному каталогу `.docker/nginx/certs`. Если вы сейчас заглянете в этот локальный каталог, то увидите пару новых файлов — `demo.test.crt` и `demo.test.key`.

Общая структура файлов теперь должна выглядеть следующим образом:

```
docker-tutorial/
├── .docker/
│   ├── backend/
│   ├── mysql/
│   └── nginx/
│       ├── certs/
│       │   ├── .gitignore
│       │   ├── demo.test.crt
│       │   └── demo.test.key
│       ├── conf.d/
│       └── Dockerfile
├── src/
├── .env
├── .env.example
├── .gitignore
├── demo
└── docker-compose.yml
```

## Установка сертификата

Давайте теперь реализуем функцию `cert_install`, которая вызывается в файле `demo` (после `cert_generate`):

```bash
# Install the certificate
cert_install () {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain .docker/nginx/certs/demo.test.crt
    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        sudo ln -s "$(pwd)/.docker/nginx/certs/demo.test.crt" /usr/local/share/ca-certificates/demo.test.crt
        sudo update-ca-certificates
    else
        echo "Could not install the certificate on the host machine, please do it manually"
    fi
}
```

Если вы работаете на macOS или на дистрибутиве Linux на базе Debian, эта функция автоматически установит самоподписанный сертификат на вашу машину. К сожалению, пользователям Windows придется делать это вручную, но с помощью [этого руководства](https://www.thewindowsclub.com/manage-trusted-root-certificates-windows) процесс будет достаточно простым (вам потребуется пройти примерно половину пути, до того момента, когда начнется разговор о _редакторе объектов групповой политики_).

!!! note "Примечание"

    Используете WSL?

    Даже если вы запустили свой проект через WSL и сертификат, казалось бы, правильно установился на вашем дистрибутиве Linux, вы, скорее всего, всё равно обращаетесь к URL через браузер из Windows. Чтобы он распознал и принял сертификат, вам необходимо скопировать соответствующий файл из Linux в Windows и выполнить ручную установку, как описано в вышеупомянутом руководстве.

Давайте разберем функцию `cert_install`: сначала она проверяет, является ли текущая хост-система macOS, проверяя содержимое предопределенной переменной окружения `$OSTYPE`, которая в этом случае будет начинаться с `darwin`. Затем он добавляет сертификат в список доверенных сертификатов.

Если текущая система — Linux, функция создаст символическую ссылку между сертификатом и папкой `/usr/local/share/ca-certificates` и запустит `update-ca-certificates`, чтобы она была принята во внимание. Обратите внимание, что этот код будет работать только для дистрибутивов на базе Debian — если вы используете другой дистрибутив, вам нужно будет соответствующим образом адаптировать условие `if` или добавить дополнительные условия, чтобы охватить больше дистрибутивов.

Поскольку в обоих случаях используется программа `sudo`, выполнение команды, вероятно, потребует ввода пароля вашей системной учётной записи.

Давайте попробуем установить сертификат (вы также можете запустить эту команду на Windows, но вам будет предложено установить сертификат вручную, как упоминалось ранее):

```bash
$ demo cert install
```

## Конфигурации сервера Nginx

Теперь, когда наш сертификат готов, нам нужно обновить конфигурацию сервера Nginx, чтобы включить поддержку HTTPS.

Сначала обновите содержимое файла `.docker/nginx/conf.d/backend.conf`:

```nginx
server {
    listen      443 ssl http2;
    listen      [::]:443 ssl http2;
    server_name backend.demo.test;
    root        /var/www/backend/public;

    ssl_certificate     /etc/nginx/certs/demo.test.crt;
    ssl_certificate_key /etc/nginx/certs/demo.test.key;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";

    index index.html index.htm index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass  backend:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include       fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}

server {
    listen      80;
    listen      [::]:80;
    server_name backend.demo.test;
    return      301 https://$server_name$request_uri;
}
```

Затем измените содержимое файла `.docker/nginx/conf.d/frontend.conf` на следующее:

```nginx
server {
    listen      443 ssl http2;
    listen      [::]:443 ssl http2;
    server_name frontend.demo.test;

    ssl_certificate     /etc/nginx/certs/demo.test.crt;
    ssl_certificate_key /etc/nginx/certs/demo.test.key;

    location / {
        proxy_pass         http://frontend:8080;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   Host $host;
    }
}

server {
    listen      80;
    listen      [::]:80;
    server_name frontend.demo.test;
    return      301 https://$server_name$request_uri;
}
```

Наконец, замените содержимое файла `.docker/nginx/conf.d/phpmyadmin.conf` на следующее:

```nginx
server {
    listen      443 ssl http2;
    listen      [::]:443 ssl http2;
    server_name phpmyadmin.demo.test;
    root        /var/www/phpmyadmin;
    index       index.php;

    ssl_certificate     /etc/nginx/certs/demo.test.crt;
    ssl_certificate_key /etc/nginx/certs/demo.test.key;
    location ~* \.php$ {

        fastcgi_pass   phpmyadmin:9000;
        root           /var/www/html;
        include        fastcgi_params;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param  SCRIPT_NAME     $fastcgi_script_name;
    }
}

server {
    listen      80;
    listen      [::]:80;
    server_name phpmyadmin.demo.test;
    return      301 https://$server_name$request_uri;
}
```

Принцип работы всех трех блоков схож: в конце добавлен второй блок `server`, который слушает трафик на порту 80 и перенаправляет его на порт 443, который обрабатывается первым блоком `server`. Последний практически не отличается от того, который он заменяет, за исключением добавления ключей конфигурации `ssl_certificate` и `ssl_certificate_key`, а также появления `http2`.

До сих пор мы не могли использовать HTTP2, потому что, хотя шифрование не требуется протоколом, на практике [большинство браузеров поддерживают его только через зашифрованное соединение](https://http2.github.io/faq/#does-http2-require-encryption). Внедрив HTTPS в нашу установку, мы теперь можем воспользоваться [улучшениями HTTP2](https://www.digitalocean.com/community/tutorials/http-1-1-vs-http-2-what-s-the-difference).

Нам также нужно внести небольшое изменение в `src/frontend/src/App.vue`, где конечная точка бэкенда теперь должна использовать HTTPS вместо HTTP:

```js
...
mounted () {
  axios
    .get('https://backend.demo.test/api/hello-there')
    .then(response => (this.msg = response.data))
}
...
```

И обновить порт в `src/frontend/vite.config.js`:

```js
...
  server: {
    host: true,
    hmr: {port: 443},
    port: 8080,
    watch: {
      usePolling: true
    }
  }
...
```

Похоже, мы готовы к тестированию! Перезапустите контейнеры, чтобы изменения вступили в силу:

```bash
$ demo restart
```

Зайдите на [frontend.demo.test](http://frontend.demo.test/) (помните, что запуск сервера разработки Vue.js может занять несколько секунд — вы можете выполнить `demo logs frontend`, чтобы проследить за происходящим): вы должны быть автоматически перенаправлены с HTTP на HTTPS, и сайт должен отображаться корректно.

Мы зашифрованы!

!!! note "Примечание"

    Не работает в вашем браузере?

    В то время как Chrome, похоже, без проблем принимает самоподписанные сертификаты на всех платформах, Firefox может выдать предупреждение о безопасности. В этом случае вам может понадобиться установить свойство `security.enterprise_roots.enabled` в `true` на странице [about:config](about:config) — после этого перезапуск браузера обычно достаточен, чтобы предупреждение исчезло (подробнее об этом параметре конфигурации читайте [здесь](https://support.mozilla.org/en-US/questions/1175296)).

    Однако с Safari оказалось сложнее: на macOS (и, возможно, на других системах) даже после игнорирования предупреждения о безопасности и принятия сертификата для обычных запросов браузера, AJAX-запросы по-прежнему не выполняются. Я пока не нашел решения, но я и не тратил много времени на поиски, потому что, если честно, мне всё равно, работает ли это в Safari (по крайней мере, локально). Если вы найдете способ, пожалуйста, сообщите мне об этом в комментариях.

    Наконец, если ваш браузер по-прежнему не принимает сертификат, я могу только посоветовать вам поискать в интернете решения о том, как установить самоподписанный сертификат для вашей конкретной установки. Поведение может варьироваться в зависимости от системы, браузера и его версии, и было бы напрасно пытаться перечислить здесь все возможные проблемы. Как я уже говорил в начале этой статьи, к сожалению, локальный HTTPS не всегда прост.

## Автоматизация процесса

Теперь, когда у нас есть функции Bash для генерации и установки сертификата, мы можем интегрировать их в процесс инициализации проекта.

Снова откройте файл `demo` и обновите функцию `init`:

```bash
# Initialise the Docker environment and the application
init () {
    env \
        && down -v \
        && build \
        && docker compose run --rm --entrypoint="//opt/files/init" backend \
        && yarn install

    if [ ! -f .docker/nginx/certs/demo.test.crt ]; then
        cert_generate
    fi

    start && cert_install
}
```

Теперь функция будет проверять, есть ли сертификат в папке `.docker/nginx/certs`, генерировать его, если нет, а затем приступит к запуску контейнеров и установке сертификата. Другими словами, теперь обо всем этом будет заботиться `demo init`.

## Трафик между контейнерами

Приведенная выше настройка подходит для большинства случаев, но есть ситуация, когда она не работает, а именно, когда контейнер должен взаимодействовать с другим контейнером напрямую, без использования браузера. Позвольте мне провести вас через это.

Во-первых, запустите проект, если он в данный момент остановлен (`demo start`), и получите доступ к контейнеру backend:

```bash
$ docker compose exec backend sh
```

Оттуда попробуйте пропинговать контейнер frontend:

```bash
$ ping frontend
```

В ответ на запрос ping должен прийти частный IP-адрес внешнего контейнера, что является ожидаемым поведением. Попробуйте снова выполнить ping для frontend, на этот раз используя доменное имя:

```bash
$ ping frontend.demo.test
```

Мы также получаем ответ, но от localhost, что не совсем правильно: вместо него мы должны получить тот же частный IP-адрес.

Давайте проведем ещё несколько тестов, по-прежнему из контейнера backend, но используя команды cURL:

```bash
$ curl frontend
```

Ответ:

```bash
curl: (7) Failed to connect to frontend port 80: Connection refused
```

Это ожидаемо, поскольку контейнер frontend настроен на прослушивание порта 8080:

```bash
$ curl frontend:8080
```

Эта команда правильно возвращает HTML-код фронтенда. Давайте попробуем ещё раз, но на этот раз используя доменное имя:

```bash
$ curl frontend.demo.test
```

Ответ:

```bash
curl: (7) Failed to connect to frontend.demo.test port 80: Connection refused
```

Та же проблема, что и выше — вместо этого мы должны использовать порт 8080:

```bash
$ curl frontend.demo.test:8080
```

Ответ:

```bash
curl: (7) Failed to connect to frontend.demo.test port 8080: Connection refused
```

Всё ещё не работает... что происходит?

Контейнеры идентифицируют друг друга по имени (например, `frontend`, `backend`, `mysql` и т. д.) в сети, созданной Docker Compose. Доменные имена, которые мы определили для frontend и backend (`frontend.demo.test` и `backend.demo.test`), распознаются нашей локальной машиной, поскольку мы обновили её файл `hosts`, но они не имеют никакого значения в контексте сети Docker Compose. Другими словами, чтобы эти доменные имена были распознаны в сети, нам нужно будет обновить `hosts`-файлы контейнеров, и делать это придется каждый раз, когда контейнеры будут создаваться заново.

К счастью, Docker Compose предлагает лучшее решение для этого, в виде [сетевых псевдонимов](https://docs.docker.com/compose/compose-file/#aliases). Псевдонимы — это альтернативные имена, которые мы можем дать сервисам и по которым их контейнеры будут обнаруживаться в сети, в дополнение к оригинальному имени сервиса. Эти псевдонимы могут быть доменными именами.

Для того чтобы как можно точнее эмулировать продакшен-среду, мы должны назначить доменное имя фронтенда сервису Nginx, а не непосредственно сервису фронтенда.

Возможно, всё становится немного запутанным, поэтому давайте вернемся к нашей диаграмме:

![](docker_frontend_to_browser.jpg)

Эта слегка обновленная версия описывает, что происходит при первом обращении к [frontend.demo.test](https://frontend.demo.test/): браузер запрашивает у Nginx содержимое фронтенда через порт 443; Nginx распознает доменное имя и передает запрос контейнеру фронтенда на порт 8080, который, в свою очередь, возвращает браузеру файлы для загрузки.

С этого момента в браузере запускается копия фронтенда:

![](docker_frontend_in_browser.jpg)

Когда конечный пользователь взаимодействует с фронтендом, запросы поступают к бэкенду:

![](docker_browser_to_backend.jpg)

Эти запросы приходят к контейнеру Nginx на порт 443, где Nginx распознает доменное имя бэкенда и проксирует запросы к контейнеру бэкенда на порт 9000.

Однако мы пытаемся достичь прямого взаимодействия между контейнерами бэкенда и фронтенда, без участия браузера:

![](docker_backend_to_frontend.jpg)

Красный маршрут (стрелка справа) уже функционирует: поскольку контейнеры frontend и backend находятся в одной сети Docker Compose, и поскольку они могут определить друг друга по имени в этой сети, backend может связаться с frontend напрямую через порт 8080. В продакшен-среде, однако, фронтенд и бэкенд вряд ли будут находиться в такой сети, и, скорее всего, будут связываться друг с другом по доменному имени (здесь я добровольно опускаю не-HTTP протоколы).

В основном они будут использовать тот же маршрут, что и браузер, через Nginx и по HTTPS — синий маршрут.

Поэтому мы хотим, чтобы доменное имя фронтенда разрешалось в контейнер Nginx, а не непосредственно во фронтенд, то есть псевдоним доменного имени должен быть назначен сервису Nginx.

Давайте добавим секцию `networks` в `docker-compose.yml`:

```yaml
# Nginx Service
nginx:
  build: ./.docker/nginx
  ports:
    - 80:80
    - 443:443
  networks:
    default:
      aliases:
        - frontend.demo.test
  volumes:
    - ./src/backend:/var/www/backend
    - ./.docker/nginx/conf.d:/etc/nginx/conf.d
    - phpmyadmindata:/var/www/phpmyadmin
    - ./.docker/nginx/certs:/etc/nginx/certs
  depends_on:
    - backend
    - frontend
    - phpmyadmin
```

Чтобы изменения вступили в силу, сеть должна быть создана заново:

```bash
$ demo down && demo start
```

Теперь мы можем приступить к тем же тестам, что и ранее, начиная с пинга:

```bash
$ docker compose exec backend sh
$ ping frontend.demo.test
```

Теперь команда отвечает правильным частным IP-адресом. Давайте попробуем с помощью cURL:

```bash
$ curl frontend.demo.test
```

Мы получаем ответ, но 301 Moved Permanently, что вполне ожидаемо — если вы помните, мы добавили второй блок `server` в каждый конфиг Nginx, отвечающий за перенаправление HTTP-трафика на HTTPS.

Давайте запустим вместо этого HTTPS URL:

```bash
$ curl https://frontend.demo.test
```

Ответ:

```bash
curl: (60) SSL certificate problem: self signed certificate
```

Теперь мы подошли к проблеме, о которой я говорил в самом начале этого раздела. Наш браузер знает и принимает самоподписанный сертификат, потому что мы установили его на нашей локальной машине; с другой стороны, внутренний контейнер не имеет понятия, откуда взялся этот сертификат, и у него нет причин доверять ему.

Простой способ обойти это — полностью игнорировать проверки безопасности:

```bash
$ curl -k https://frontend.demo.test
```

Хотя это решение работает, оно не рекомендуется по очевидным причинам безопасности, и у вас не всегда есть возможность установить опции по своему усмотрению (особенно если вызов выполняется сторонним пакетом).

На самом деле нам нужно установить сертификат и на внутренний контейнер, чтобы он мог распознать его и доверять ему так же, как это делает наша локальная машина.

Для этого нам нужно смонтировать каталог с самоподписанным сертификатом на внутреннем контейнере. Выйдите из контейнера (выполнив команду `exit` или нажав `ctrl + d`) и обновите `docker-compose.yml`:

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
```

Сохраните файл и перезапустите контейнеры:

```bash
$ demo restart
```

Снова зайдите в контейнер backend и установите новый сертификат (предупреждение можно проигнорировать):

```bash
$ docker compose exec -u root backend sh
$ update-ca-certificates
```

Обратите внимание на опцию `-u` в первой команде выше — `update-ca-certificates` требует привилегий root, которых нет у пользователя контейнера по умолчанию (`demo`). Опция `-u` позволяет нам получить доступ к контейнеру от имени другого пользователя (`root`), чтобы мы могли запустить `update-ca-certificates` с нужными правами.

Попробуйте выполнить команду cURL ещё раз:

```bash
$ curl https://frontend.demo.test
```

В итоге вы должны получить HTML-код фронтенда.

Есть ещё одна вещь, которую нам нужно сделать перед завершением работы. Обновите функцию `cert_install` в файле `demo`:

```bash
# Install the certificate
cert_install () {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain .docker/nginx/certs/demo.test.crt
    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        sudo ln -s "$(pwd)/.docker/nginx/certs/demo.test.crt" /usr/local/share/ca-certificates/demo.test.crt
        sudo update-ca-certificates
    else
        echo "Could not install the certificate on the host machine, please do it manually"
    fi

    docker compose exec -u root backend update-ca-certificates
}
```

После установки сертификата на локальной машине функция теперь будет делать то же самое на внутреннем контейнере.

!!! note "Примечание"

    Почему это важно?

    Должен признаться, что приведенный выше пример не самый подходящий, поскольку на практике я не могу придумать ни одной причины, по которой бэкенд должен взаимодействовать с фронтендом таким образом. Однако взаимодействие контейнера с контейнером — не такая уж редкая вещь: типичные случаи использования включают приложения, запрашивающие сервер аутентификации (вспомните OAuth), или микросервисы, взаимодействующие через HTTP. Я просто не хотел удлинять этот учебник, вводя ещё один контейнер.

    Тем не менее, я бы рекомендовал устанавливать сертификат на контейнер только в случае крайней необходимости, поскольку это дополнительный шаг, о котором легко забыть. Если вам по какой-то причине понадобится заново создать контейнер, вам также придется не забыть запустить `demo cert install`; на момент написания статьи не существует таких событий контейнера, как создание контейнера, которые можно было бы автоматизировать.

## Заключение

Будем откровенны: работа с HTTPS на локальном уровне — это всё ещё боль в горле. К сожалению, без него среда разработки была бы неполной, поскольку он стал практически обязательным требованием современного Интернета.

Однако в этом есть и положительная сторона: теперь, когда с шифрованием покончено, в этой серии уроков осталось только самое интересное. Радуйтесь!

В [следующей части](../docker-dlja-lokalnoj-veb-razrabotki-chast-6/index.md) мы рассмотрим, как вывести локальный контейнер в Интернет, что очень удобно при тестировании интеграции стороннего сервиса.

---

Оригинальная статья: [Docker for local web development, part 5: HTTPS all the things](https://tech.osteel.me/posts/docker-for-local-web-development-part-5-https-all-the-things) (English)
