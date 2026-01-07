---
title: Разработка Laravel-проектов на основе API
description: Советы и идеи по созданию API с помощью Laravel
slug: razrabotka-laravel-proektov-na-osnove-api
date: 2026-01-07
tags:
  - Laravel
  - API
---

Перевод статьи Стива Макдугалла «API-First Laravel Projects» — о создании API-ориентированных проектов Laravel.

<!-- more -->

## Введение

Я создаю API на Laravel уже много лет, и одна вещь стала очевидной: то, как мы изучаем Laravel, не поспевает за тем, как мы на самом деле его используем. Большинство руководств для начинающих до сих пор сосредоточены на полнофункциональных приложениях с представлениями Blade, готовой системой аутентификации и страницами, отрисованными на сервере. Это хорошо для понимания основ Laravel, но реальность современной разработки другая.

Сегодня Laravel — это бэкенд. Он обслуживает фронтенды на React, приложения на Vue, мобильные приложения и сторонние интеграции. Он говорит на JSON, а не на HTML. Понимание того, как создавать чистые и поддерживаемые API, больше не является приятным дополнением — это основа.

Это руководство представляет десять последовательных проектов, разработанных для обучения разработке API на Laravel. Каждый проект опирается на концепции из предыдущих, вводя новые паттерны и задачи, с которыми вы столкнётесь в реальных приложениях. Не буду скрывать: некоторые из них вас разочаруют. Это хорошо. Борьба с этими концепциями сейчас означает, что вам не придётся изучать их позже под давлением дедлайнов.

### Почему эти проекты важны

Прежде чем мы начнём, давайте поговорим о том, что отличает эти проекты от типичных руководств для начинающих.

Во-первых, они ориентированы на API. Вы не создадите ни одного представления Blade. Каждое взаимодействие происходит через HTTP-эндпойнты, возвращающие JSON. Это заставляет вас думать об управлении состоянием, аутентификации и преобразовании данных иначе, чем в традиционном веб-приложении.

Во-вторых, они последовательные. Первый проект учит базовому CRUD. Десятый включает вебхуки, очереди и сложное управление состоянием. Не пропускайте шаги. Паттерны, которые вы изучите в начале, усложняются в более продвинутых проектах.

В-третьих, они намеренно неполные. Я даю вам структуру и ключевые концепции, но не буду водить вас за руку через каждую строку кода. Вам нужно будет читать документацию, принимать решения и иногда рефакторить, когда вы поймёте, что ваш первый подход был не идеальным. Это не баг — так вы на самом деле учитесь.

## Проект 1: API для задач - Учимся мыслить ресурсами

Ключевые концепции: CRUD-операции, ресурсы API, HTTP-коды состояния, валидация

Начнём с простого. Создайте API для управления задачами. Это намеренно базовый проект, потому что цель не в сложности предметной области — а в изучении того, как Laravel обрабатывает API-ответы.

Эндпойнты

```yaml
GET    /api/tasks       # Список всех задач
POST   /api/tasks       # Создание новой задачи
GET    /api/tasks/{id}  # Получение конкретной задачи
PUT    /api/tasks/{id}  # Обновление задачи
DELETE /api/tasks/{id}  # Удаление задачи
```

Стандартные REST-соглашения. Ничего удивительного. Но вот где новички обычно ошибаются: они возвращают модели напрямую.

```php
<?php

// Не делайте так!
public function index()
{
    return Task::all();
}
```

Это работает, конечно. Но это негибко и напрямую раскрывает структуру вашей базы данных потребителям API. Что произойдёт, когда вы переименуете столбец? Что если вам нужно форматировать даты единообразно? А как насчёт вычисляемых значений?

Вот для чего нужны ресурсы API. Это слои преобразования, которые находятся между вашими моделями и JSON-ответами.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TaskResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'           => $this->id,
            'title'        => $this->title,
            'description'  => $this->description,
            'completed'    => (bool) $this->completed,
            'completed_at' => $this->completed_at?->toISOString(),
            'created_at'   => $this->created_at->toISOString(),
            'updated_at'   => $this->updated_at->toISOString(),
        ];
    }
}
```

Теперь ваш контроллер выглядит так:

```php
<?php

public function index()
{
    return TaskResource::collection(
        Task::all()
    );
}

public function show(Task $task)
{
    return new TaskResource($task);
}
```

Видите разницу? Теперь структура ответа вашего API отвязана от схемы базы данных. Вы можете менять структуру БД, не ломая внешний контракт вашего API. Такое разделение становится критически важным по мере роста приложения.

### Валидация, которая реально помогает

`Form Request`‑классы — ваши друзья. Не выполняйте валидацию прямо в контроллерах.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreTaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title'       => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'completed'   => ['boolean'],
        ];
    }
}
```

Затем используйте этот класс в контроллере:

```php
<?php

public function store(StoreTaskRequest $request)
{
    $task = Task::create($request->validated());

    return new TaskResource($task);
}
```

Laravel автоматически возвращает код 422 с ошибками валидации, если запрос не проходит проверку. Вам не нужно писать этот код — это просто происходит. Это одно из тех удобств Laravel, которые делают разработку API приятной.

### Проблема кодов состояния

HTTP-коды состояния имеют значение. Большое значение. Клиентам вашего API необходимо программно понимать, что произошло, без разбора текстов сообщений об ошибках.

```php
<?php

// Создание ресурса
return (new TaskResource($task))
    ->response()
    ->setStatusCode(201);

// Успешное удаление
return response()->json(null, 204);

// Не найдено (обрабатывается автоматически благодаря привязке модели к маршруту)
return response()->json([
    'message' => 'Task not found'
], 404);
```

Освойтесь с кодами `200 (OK)`, `201 (Created)`, `204 (No Content)`, `400 (Bad Request)`, `404 (Not Found)` и `422 (Unprocessable Entity)`. Вы будете использовать их постоянно.

### Что вы на самом деле изучаете

Этот проект не о управлении задачами. Он о понимании цикла «запрос-ответ» в контексте API. Он о том, чтобы узнать, что Laravel предоставляет инструменты, предназначенные для разработки API, и что их использование облегчает вам жизнь.

Не переходите дальше, пока не сможете создать этот API и протестировать его с помощью инструмента вроде Postman или Insomnia. Реально отправляйте запросы. Смотрите, какие ответы получаете. Ломайте всё намеренно, чтобы понять ответы с ошибками.

## Проект 2: API блога с категориями - Осваиваем отношения

Ключевые концепции: отношения Eloquent, жадная загрузка, фильтрация, пагинация, проблема N+1 запросов

Теперь добавляем сложность. Посты принадлежат категориям. Авторы пишут посты. Здесь вы начинаете видеть реальную мощь Eloquent, и здесь же вы столкнётесь с первыми проблемами производительности, если не будете осторожны.

Схема:

```php
<?php

Schema::create('categories', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('slug')->unique();
    $table->timestamps();
});

Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('category_id')->constrained();
    $table->foreignId('user_id')->constrained();
    $table->string('title');
    $table->string('slug')->unique();
    $table->text('content');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
});
```

Достаточно просто. Но отношения — вот где всё становится интересным.


```php
<?php

class Post extends Model
{
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }
}

class Category extends Model
{
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

### Проблема N+1

Вот контроллер, который выглядит нормально, но убьёт вашу базу данных:

```php
<?php

public function index()
{
    $posts = Post::all();

    return PostResource::collection($posts);
}
```

Если ваш `PostResource` включает название категории, вы только что создали проблему N+1 запросов. Laravel выполнит один запрос для получения всех постов, а затем по одному дополнительному запросу для каждого поста, чтобы получить его категорию. При 100 постах это будет 101 запрос.

Решение — жадная загрузка:


```php
<?php

public function index()
{
    $posts = Post::with(['category', 'author'])->get();

    return PostResource::collection($posts);
}
```

Теперь Laravel выполняет всего три запроса: один для постов, один для всех категорий, один для всех авторов. Затем он сопоставляет их в PHP. Это разница между быстрым и медленным API.

Включите логирование запросов в режиме разработки, чтобы увидеть это:

```php
<?php

DB::listen(function ($query) {
    Log::info($query->sql);
});
```

Вы удивитесь, сколько запросов генерирует ваш безобидно выглядящий код.

### Фильтрация и пагинация

Реальным API нужна фильтрация. Пользователям нужны посты из конкретной категории, или опубликованные посты, или посты за определённый период. Не захардкодивайте это — сделайте гибким.

```php
<?php

public function index(Request $request)
{
    $query = Post::with(['category', 'author']);

    if ($request->has('category')) {
        $query->whereHas('category', function ($q) use ($request) {
            $q->where('slug', $request->category);
        });
    }

    if ($request->has('author')) {
        $query->where('user_id', $request->author);
    }

    if ($request->boolean('published')) {
        $query->whereNotNull('published_at');
    }

    return PostResource::collection(
        $query->latest()->paginate(15)
    );
}
```

Обратите внимание на вызов `paginate()`. Никогда не возвращайте неограниченные коллекции. Всегда используйте пагинацию. Пагинация Laravel автоматически включает метаданные и ссылки в JSON-ответ, которые ваш фронтенд может использовать для построения элементов управления пагинацией.

### Вложенные ресурсы

Должны ли категории иметь собственный эндпойнт для постов? Да.

```php
<?php

Route::get('categories/{category}/posts', function (Category $category) {
    return PostResource::collection(
        $category->posts()->with('author')->latest()->paginate()
    );
});
```

Это чище, чем фильтрация в основном списке постов. Это также более семантично — вы запрашиваете «посты в этой категории», а не «посты, отфильтрованные по категории». Разница имеет значение, когда вы создаёте интуитивно понятный API.

### Что вы изучаете

Отношения — это суперсила Eloquent, но это также то место, где скрываются проблемы производительности. Этот проект учит вас думать о запросах, а не только о моделях. Он учит вас, что `->with()` почти всегда необходим. Он учит вас, что пагинация не является опциональной.

Вы также узнаёте, что проектирование API включает компромиссы. Включать ли полный объект категории в ответ поста или только ID категории? Универсально правильного ответа не существует — это зависит от вашего случая использования.

## Проект 3: API менеджера закладок - Правильная аутентификация

Ключевые концепции: Laravel Sanctum, токен-аутентификация, защищённые маршруты, данные с привязкой к пользователю

Здесь ваш API становится реальным. Пользователи могут регистрироваться, входить в систему и управлять своими собственными данными. Другие пользователи не могут их видеть. Это основа каждого SaaS-приложения, которое вы когда-либо создадите.

### Настройка Sanctum

Laravel Sanctum создан именно для этого случая: токен-аутентификация для SPA и мобильных приложений. Он проще, чем Passport, и идеален для большинства приложений.

```sh
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate
```

Добавьте мидлвар Sanctum в вашу группу мидлваров для API в `app/Http/Kernel.php`:

```php
<?php

'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

И добавьте трейт `HasApiTokens` в вашу модель `User`:

```php
<?php

use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
    // ...
}
```

### Регистрация и вход

Вот базовый эндпойнт регистрации:

```php
<?php

public function register(Request $request)
{
    $request->validate([
        'name'     => ['required', 'string', 'max:255'],
        'email'    => ['required', 'string', 'email', 'max:255', 'unique:users'],
        'password' => ['required', 'string', 'min:8', 'confirmed'],
    ]);

    $user = User::create([
        'name'     => $request->name,
        'email'    => $request->email,
        'password' => Hash::make($request->password),
    ]);

    $token = $user->createToken('auth-token')->plainTextToken;

    return response()->json([
        'user'  => new UserResource($user),
        'token' => $token,
    ], 201);
}
```

И вход:

```php
<?php

public function login(Request $request)
{
    $request->validate([
        'email'    => ['required', 'email'],
        'password' => ['required'],
    ]);

    if (!Auth::attempt($request->only('email', 'password'))) {
        return response()->json([
            'message' => 'Invalid credentials'
        ], 401);
    }

    $user  = User::where('email', $request->email)->firstOrFail();
    $token = $user->createToken('auth-token')->plainTextToken;

    return response()->json([
        'user'  => new UserResource($user),
        'token' => $token,
    ]);
}
```

Клиенты вашего API сохраняют этот токен и отправляют его с каждым запросом:

```yaml
Authorization: Bearer {token}
```

### Защита маршрутов

Теперь оберните маршруты закладок в аутентификацию:


```php
<?php

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('bookmarks', BookmarkController::class);
});
```

Вот и всё. Любой запрос к этим маршрутам без действительного токена автоматически получает ответ 401.

### Привязка данных к пользователям

Это критически важно. Пользователи должны видеть только свои собственные закладки. Каждый запрос требует привязки:

```php
<?php

public function index(Request $request)
{
    return BookmarkResource::collection(
        $request->user()->bookmarks()->latest()->paginate()
    );
}

public function store(Request $request)
{
    $bookmark = $request->user()->bookmarks()->create(
        $request->validated()
    );

    return new BookmarkResource($bookmark);
}
```

Обратите внимание, что мы используем `$request->user()` для получения аутентифицированного пользователя, а затем получаем доступ к его закладкам через отношение. Это гарантирует, что пользователи не смогут получить доступ к данным других пользователей.

Для операций обновления и удаления вам нужны политики авторизации:

```php
<?php

public function update(Request $request, Bookmark $bookmark)
{
    $this->authorize('update', $bookmark);

    $bookmark->update($request->validated());

    return new BookmarkResource($bookmark);
}
```

И политика:

```php
<?php

public function update(User $user, Bookmark $bookmark): bool
{
    return $user->id === $bookmark->user_id;
}
```

Laravel проверяет это автоматически. Если политика возвращает `false`, Laravel возвращает ответ `403 Forbidden`. Вам не нужно писать этот код.

### Что вы изучаете

Аутентификация — это базовое требование для любого реального приложения. Этот проект учит вас, как правильно реализовать её с помощью современных инструментов Laravel. Вы узнаёте, что аутентификация (кто вы?) и авторизация (что вы можете делать?) — это разные концепции, и Laravel элегантно справляется с обеими.

Вы также узнаёте, что безопасность — это не дополнение, она встроена в вашу архитектуру. Привязывать запросы к аутентифицированным пользователям с самого начала проще, чем пытаться добавить это позже.

## Проект 4: API рецептов с поиском - Сложность запросов

Ключевые концепции: Полнотекстовый поиск, сложная фильтрация, диапазоны запросов, оптимизация поиска

Пользователям нужно находить рецепты. По ингредиентам. По кухне. По диетическим ограничениям. Здесь простые where-условия перестают быть достаточными, и вам нужно задуматься о том, как сделать запросы компонуемыми и поддерживаемыми.

Схема:

```php
<?php

Schema::create('recipes', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('title');
    $table->text('description');
    $table->text('instructions');
    $table->string('cuisine')->nullable();
    $table->integer('prep_time'); // in minutes
    $table->integer('cook_time');
    $table->integer('servings');
    $table->json('dietary_info')->nullable(); // ['vegetarian', 'gluten-free']
    $table->timestamps();
});

Schema::create('ingredients', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->timestamps();
});

Schema::create('ingredient_recipe', function (Blueprint $table) {
    $table->foreignId('recipe_id')->constrained()->onDelete('cascade');
    $table->foreignId('ingredient_id')->constrained()->onDelete('cascade');
    $table->string('quantity');
    $table->string('unit')->nullable();
});
```

### Диапазоны запросов сохраняют контроллеры чистыми

Не делайте так:

```php
<?php

public function index(Request $request)
{
    $query = Recipe::query();

    if ($request->has('cuisine')) {
        $query->where('cuisine', $request->cuisine);
    }

    if ($request->has('max_time')) {
        $query->where(DB::raw('prep_time + cook_time'), '<=', $request->max_time);
    }

    if ($request->has('dietary')) {
        $dietary = json_decode($request->dietary);
        $query->where(function ($q) use ($dietary) {
            foreach ($dietary as $diet) {
                $q->orWhereJsonContains('dietary_info', $diet);
            }
        });
    }

    if ($request->has('search')) {
        $search = $request->search;
        $query->where(function ($q) use ($search) {
            $q->where('title', 'like', "%{$search}%")
              ->orWhere('description', 'like', "%{$search}%");
        });
    }

    return RecipeResource::collection($query->paginate());
}
```

Этот контроллер делает слишком много. Вынесите логику запросов в диапазоны:

```php
<?php

class Recipe extends Model
{
    public function scopeCuisine($query, $cuisine)
    {
        return $query->where('cuisine', $cuisine);
    }

    public function scopeMaxTotalTime($query, $minutes)
    {
        return $query->whereRaw('(prep_time + cook_time) <= ?', [$minutes]);
    }

    public function scopeDietary($query, array $requirements)
    {
        foreach ($requirements as $requirement) {
            $query->whereJsonContains('dietary_info', $requirement);
        }

        return $query;
    }

    public function scopeSearch($query, $term)
    {
        return $query->where(function ($q) use ($term) {
            $q->where('title', 'like', "%{$term}%")
              ->orWhere('description', 'like', "%{$term}%");
        });
    }

    public function scopeWithIngredient($query, $ingredientId)
    {
        return $query->whereHas('ingredients', function ($q) use ($ingredientId) {
            $q->where('ingredient_id', $ingredientId);
        });
    }
}
```

Теперь ваш контроллер читаемый:

```php
<?php

public function index(Request $request)
{
    $query = Recipe::with(['user', 'ingredients']);

    if ($request->filled('cuisine')) {
        $query->cuisine($request->cuisine);
    }

    if ($request->filled('max_time')) {
        $query->maxTotalTime($request->max_time);
    }

    if ($request->filled('dietary')) {
        $query->dietary($request->dietary);
    }

    if ($request->filled('search')) {
        $query->search($request->search);
    }

    if ($request->filled('ingredient')) {
        $query->withIngredient($request->ingredient);
    }

    return RecipeResource::collection(
        $query->latest()->paginate()
    );
}
```

Каждый диапазон переиспользуемый, тестируемый и выразительный. Так вы сохраняете контроллеры тонкими, а запросы поддерживаемыми.

### Полнотекстовый поиск с помощью Scout

Подход с `LIKE` работает для небольших наборов данных, но он не масштабируется. Для настоящего поиска используйте Laravel Scout с драйвером вроде Meilisearch или Algolia.

```sh
composer require laravel/scout
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

Сделайте вашу модель доступной для поиска:

```php
<?php

use Laravel\Scout\Searchable;

class Recipe extends Model
{
    use Searchable;

    public function toSearchableArray()
    {
        return [
            'id'          => $this->id,
            'title'       => $this->title,
            'description' => $this->description,
            'cuisine'     => $this->cuisine,
            'ingredients' => $this->ingredients->pluck('name')->toArray(),
        ];
    }
}
```

Тогда поиск становится таким:

```php
<?php

$recipes = Recipe::search($request->search)
    ->query(fn ($query) => $query->with('ingredients'))
    ->paginate();
```

Scout берёт на себя тяжёлую работу. Он автоматически синхронизирует вашу базу данных с поисковым индексом.

### Что вы изучаете

Этот проект об управлении сложностью. По мере того как ваши запросы становятся более сложными, вам нужны паттерны для их поддержки. Диапазоны запросов — один из таких паттернов. Они позволяют вам составлять запросы из небольших, понятных частей.

Вы также узнаёте, что для некоторых задач нужны специализированные инструменты. Полнотекстовый поиск с `LIKE` подходит для демонстраций, но реальным приложениям нужна настоящая поисковая инфраструктура. Экосистема Laravel предоставляет это, не заставляя вас изобретать велосипед.

## Проект 5: API трекера расходов с отчётами - Агрегация данных

Ключевые концепции: Агрегации базы данных, фильтрация по датам, группировка, преобразование данных, вычисляемые значения

API не просто возвращают сырые данные — им часто нужно выполнять вычисления и преобразования. Этот проект учит вас, как использовать конструктор запросов Laravel для агрегаций и как структурировать сложные аналитические данные в ответах вашего API.

### Предметная область

Пользователи отслеживают расходы. Каждый расход имеет сумму, категорию, дату и необязательные примечания. API должен предоставлять не просто список расходов, но и агрегированные отчёты: итоги по категориям, месячные сводки, сравнения год к году.

```php
<?php

Schema::create('expenses', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->foreignId('category_id')->constrained();
    $table->decimal('amount', 10, 2);
    $table->date('date');
    $table->string('description')->nullable();
    $table->timestamps();
});

Schema::create('categories', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('name');
    $table->string('color')->nullable();
    $table->timestamps();
});
```

### Базовые агрегации

Получение итогов по категориям:

```php
<?php

public function categoryTotals(Request $request)
{
    $totals = $request->user()
        ->expenses()
        ->selectRaw('category_id, SUM(amount) as total')
        ->groupBy('category_id')
        ->with('category:id,name,color')
        ->get();

    return response()->json([
        'data' => $totals->map(fn ($item) => [
            'category' => [
                'id'    => $item->category->id,
                'name'  => $item->category->name,
                'color' => $item->category->color,
            ],
            'total' => (float) $item->total,
        ])
    ]);
}
```

Обратите внимание на `selectRaw` и `groupBy`. Это SQL-функции агрегации, и они мощные. Но это также означает, что вы больше не получаете полные Eloquent-модели — вы получаете частичные модели только с выбранными полями.

### Фильтрация по диапазону дат

```php
<?php

public function summary(Request $request)
{
    $request->validate([
        'start_date' => ['required', 'date'],
        'end_date'   => ['required', 'date', 'after_or_equal:start_date'],
    ]);

    $expenses = $request->user()
        ->expenses()
        ->whereBetween('date', [$request->start_date, $request->end_date])
        ->with('category')
        ->get();

    return response()->json([
        'period'         => [
            'start' => $request->start_date,
            'end'   => $request->end_date,
        ],
        'total_expenses' => $expenses->sum('amount'),
        'count'          => $expenses->count(),
        'average'        => $expenses->avg('amount'),
        'by_category'    => $expenses->groupBy('category_id')->map(function ($items) {
            return [
                'category' => $items->first()->category->name,
                'total'    => $items->sum('amount'),
                'count'    => $items->count(),
            ];
        })->values(),
    ]);
}
```

Это использует методы коллекций для агрегации вместо запросов к базе данных. Для небольших наборов данных это нормально и часто более гибко. Для больших наборов данных вы бы хотели переложить агрегацию на базу данных.

### Месячные отчёты

```php
<?php

public function monthlyReport(Request $request, int $year)
{
    $expenses = $request->user()
        ->expenses()
        ->whereYear('date', $year)
        ->selectRaw('MONTH(date) as month, SUM(amount) as total, COUNT(*) as count')
        ->groupBy('month')
        ->orderBy('month')
        ->get();

    // Заполняем отсутствующие месяцы нулями
    $months = collect(range(1, 12))->map(function ($month) use ($expenses) {
        $data = $expenses->firstWhere('month', $month);

        return [
            'month'      => $month,
            'month_name' => Carbon::create()->month($month)->format('F'),
            'total'      => $data ? (float) $data->total : 0,
            'count'      => $data ? $data->count : 0,
        ];
    });

    return response()->json([
        'year'         => $year,
        'months'       => $months,
        'yearly_total' => $months->sum('total'),
    ]);
}
```

Это распространённый паттерн: запросить агрегированные данные, затем заполнить пробелы значениями по умолчанию. Без заполнения пробелов месяцы без расходов не появятся в результатах, что сломает любые графики на фронтенде.

### Что вы изучаете

Этот проект учит вас, что API — это больше, чем просто CRUD. Реальным приложениям нужно преобразовывать и агрегировать данные. Вы узнаёте, когда использовать агрегации базы данных, а когда методы коллекций. Вы узнаёте, как структурировать сложные аналитические ответы, чтобы фронтенды могли легко их использовать.

Вы также узнаёте, что работа с датами удивительно сложна. Часовые пояса, диапазоны дат и агрегация по временным периодам — всё это имеет граничные случаи. Carbon здесь ваш друг, но вам всё равно нужно тщательно думать о том, что вы вычисляете.

## Проект 6: API подтверждения участия в событиях - Сложные отношения и состояния

Ключевые концепции: Отношения «многие-ко-многим», промежуточные таблицы, управление состоянием, ограничения вместимости

Отношения «многие-ко-многим» — это то, где Eloquent действительно блистает, но это также место, где всё становится сложным. У событий есть участники. Участники могут подтвердить участие в нескольких событиях. Сама связь имеет состояние («иду», «может быть», «не иду»). У событий есть ограничения по вместимости. Это сложность реального мира.

Схема:

```php
<?php

Schema::create('events', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained(); // event creator
    $table->string('title');
    $table->text('description');
    $table->string('location');
    $table->dateTime('starts_at');
    $table->dateTime('ends_at');
    $table->integer('capacity')->nullable();
    $table->timestamps();
});

Schema::create('event_user', function (Blueprint $table) {
    $table->id();
    $table->foreignId('event_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->enum('status', ['going', 'maybe', 'not_going']);
    $table->text('note')->nullable();
    $table->timestamps();

    $table->unique(['event_id', 'user_id']);
});
```

Отношения:

```php
<?php

class Event extends Model
{
    public function creator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function attendees(): BelongsToMany
    {
        return $this->belongsToMany(User::class)
            ->withPivot('status', 'note')
            ->withTimestamps();
    }

    public function confirmed(): BelongsToMany
    {
        return $this->attendees()->wherePivot('status', 'going');
    }

    public function maybe(): BelongsToMany
    {
        return $this->attendees()->wherePivot('status', 'maybe');
    }
}

class User extends Model
{
    public function events(): BelongsToMany
    {
        return $this->belongsToMany(Event::class)
            ->withPivot('status', 'note')
            ->withTimestamps();
    }

    public function createdEvents(): HasMany
    {
        return $this->hasMany(Event::class);
    }
}
```

Обратите внимание на вызов `withPivot()`. Это указывает Eloquent включить эти столбцы из промежуточной таблицы при обращении к отношению. Без этого вы не сможете увидеть статус подтверждения участия.

### Логика подтверждения участия

```php
<?php

public function rsvp(Request $request, Event $event)
{
    $request->validate([
        'status' => ['required', 'in:going,maybe,not_going'],
        'note'   => ['nullable', 'string', 'max:500'],
    ]);

    // Проверяем вместимость, если отмечают как «going» («иду»)
    if ($request->status === 'going' && $event->capacity) {
        $confirmed = $event->confirmed()->count();

        if ($confirmed >= $event->capacity) {
            return response()->json([
                'message' => 'This event is at capacity'
            ], 422);
        }
    }

    // Прикрепляем или обновляем подтверждение участия
    $event->attendees()->syncWithoutDetaching([
        $request->user()->id => [
            'status' => $request->status,
            'note'   => $request->note,
        ]
    ]);

    return response()->json([
        'message' => 'RSVP updated successfully',
        'status'  => $request->status,
    ]);
}
```

Метод `syncWithoutDetaching` идеален здесь. Он обновляет запись в промежуточной таблице, если она существует, создаёт её, если нет, но не удаляет другие связи.

### Доступ к данным промежуточной таблицы

Когда вы получаете событие с участниками, данные промежуточной таблицы доступны:

```php
<?php

$event = Event::with('attendees')->find($id);

foreach ($event->attendees as $attendee) {
    echo $attendee->pivot->status; // 'going', 'maybe', или 'not_going'
    echo $attendee->pivot->created_at; // когда подтверждается участие
}
```

Это выводится в вашем ресурсе:

```php
<?php

class EventResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'              => $this->id,
            'title'           => $this->title,
            'description'     => $this->description,
            'starts_at'       => $this->starts_at->toISOString(),
            'capacity'        => $this->capacity,
            'attendee_count'  => $this->confirmed()->count(),
            'spots_remaining' => $this->capacity
                ? max(0, $this->capacity - $this->confirmed()->count())
                : null,
            'attendees'       => $this->whenLoaded('attendees', function () {
                return $this->attendees->map(fn ($user) => [
                    'id'      => $user->id,
                    'name'    => $user->name,
                    'status'  => $user->pivot->status,
                    'rsvp_at' => $user->pivot->created_at->toISOString(),
                ]);
            }),
        ];
    }
}
```

### Что вы изучаете

Отношения «многие-ко-многим» с данными в промежуточной таблице часто встречаются в реальных приложениях: пользователи и роли, товары и заказы, студенты и курсы. Этот проект учит вас, как правильно работать с ними в Laravel.

Вы узнаёте, что связи — это не просто ссылки между таблицами, это полноценные структуры данных с собственными атрибутами и логикой. Промежуточная таблица — это модель сама по себе, даже если вы не всегда явно определяете её как таковую.

Вы также изучаете управление состоянием на уровне базы данных. Подтверждения участия имеют состояние. События имеют ограничения по вместимости. Это не просто модели данных — это бизнес-правила, которые ваш API должен соблюдать.

## Проект 7: Мультитенантный SaaS API - Привязка всего к арендаторам

Ключевые концепции: Мультитенантность, глобальные диапазоны, доступ на основе команд, разрешения на основе ролей

Реальные SaaS-приложения являются мультитенантными. Пользователи принадлежат к командам (или организациям, рабочим пространствам, аккаунтам — выбирайте терминологию, которую предпочитаете). Все данные принадлежат команде. Пользователи могут принадлежать к нескольким командам. Это принципиально меняет структуру вашего приложения.

### Основная концепция

Каждая таблица, содержащая созданные пользователями данные, нуждается в столбце `team_id`. Каждый запрос должен быть привязан к текущей команде. Пользователи могут переключаться между командами. Это намного сложнее, чем кажется.

```php
<?php

Schema::create('teams', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('slug')->unique();
    $table->foreignId('owner_id')->constrained('users');
    $table->timestamps();
});

Schema::create('team_user', function (Blueprint $table) {
    $table->foreignId('team_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('role')->default('member');
    $table->timestamps();

    $table->primary(['team_id', 'user_id']);
});

Schema::create('projects', function (Blueprint $table) {
    $table->id();
    $table->foreignId('team_id')->constrained()->onDelete('cascade');
    $table->string('name');
    $table->text('description')->nullable();
    $table->timestamps();
});
```

### Глобальные диапазоны для автоматической фильтрации

Не добавляйте вручную `where('team_id', ...)` к каждому запросу. Используйте глобальные диапазоны:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class TeamScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        if ($teamId = $this->getCurrentTeamId()) {
            $builder->where("{$model->getTable()}.team_id", $teamId);
        }
    }

    protected function getCurrentTeamId(): ?int
    {
        return auth()->user()?->currentTeam?->id;
    }
}
```

Примените его к вашим моделям:

```php
<?php

class Project extends Model
{
    protected static function booted(): void
    {
        static::addGlobalScope(new TeamScope);
    }
}
```

Теперь каждый запрос к `Project` автоматически привязан к текущей команде. Вы не можете случайно допустить утечку данных между командами.

### Переключение между командами

Пользователям необходимо переключаться между командами. Храните текущую команду у пользователя:

```php
<?php

class User extends Model
{
    public function currentTeam(): BelongsTo
    {
        return $this->belongsTo(Team::class, 'current_team_id');
    }

    public function teams(): BelongsToMany
    {
        return $this->belongsToMany(Team::class)
            ->withPivot('role')
            ->withTimestamps();
    }

    public function switchTeam(Team $team): void
    {
        if (!$this->teams->contains($team->id)) {
            throw new \Exception('User does not belong to this team');
        }

        $this->current_team_id = $team->id;
        $this->save();
    }
}
```

Эндпойнт для переключения:

```php
<?php

public function switch(Request $request, Team $team)
{
    $request->user()->switchTeam($team);

    return response()->json([
        'message'      => 'Switched to team: ' . $team->name,
        'current_team' => new TeamResource($team),
    ]);
}
```

### Разрешения на основе ролей

Используйте пакет Laravel Permission от Spatie. Не создавайте это с нуля.

```sh
composer require spatie/laravel-permission
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
php artisan migrate
```

Определите роли и разрешения для каждой команды:

```php
<?php

$team = Team::find(1);
$user = User::find(1);

// Назначаем роль в контексте команды
$user->assignRole('admin');

// Проверяем разрешения
if ($user->hasPermissionTo('create projects')) {
    // разрешено
}

// В ваших политиках
public function create(User $user): bool
{
    return $user->hasPermissionTo('create projects');
}
```

### Что вы изучаете

Мультитенантность — это архитектурное решение, которое влияет на всё ваше приложение. Этот проект учит вас, что изоляция — это не только вопрос безопасности, но и вопрос логической корректности приложения. Пользователи никогда не должны случайно видеть данные других команд, даже если в вашем коде есть ошибка.

Вы узнаёте, что глобальные диапазоны мощны, но требуют осторожного использования. Они невидимы, что является одновременно их силой и опасностью. Вы также узнаёте, что некоторые типы задач встречаются настолько часто, что использовать уже готовые, хорошо проверенные пакеты — это самый правильный выбор.

## Проект 8: API с вебхуками - Асинхронные уведомления

Ключевые концепции: Вебхуки, события Laravel, обработчики очередей, логика повторных попыток, проверка подписи

Вебхуки позволяют вашему API уведомлять другие сервисы, когда что-то происходит. Пользователь создал аккаунт? Отправьте вебхук. Платёж обработан? Отправьте вебхук. Именно так современные API интегрируются друг с другом.

Схема:

```php
<?php

Schema::create('webhooks', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('url');
    $table->json('events'); // ['user.created', 'project.updated']
    $table->string('secret');
    $table->boolean('active')->default(true);
    $table->timestamps();
});

Schema::create('webhook_calls', function (Blueprint $table) {
    $table->id();
    $table->foreignId('webhook_id')->constrained()->onDelete('cascade');
    $table->string('event');
    $table->json('payload');
    $table->integer('response_status')->nullable();
    $table->text('response_body')->nullable();
    $table->integer('attempt')->default(1);
    $table->timestamp('delivered_at')->nullable();
    $table->timestamps();
});
```

### События и слушатели

Когда что-то происходит, запустите событие:

```php
<?php

event(new ProjectCreated($project));
```

Само событие:

```php
<?php

namespace App\Events;

use App\Models\Project;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class ProjectCreated
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public Project $project
    ) {}
}
```

Слушайте события и отправляйте вебхуки:

```php
<?php

namespace App\Listeners;

use App\Events\ProjectCreated;
use App\Jobs\SendWebhookJob;
use App\Models\Webhook;

class SendProjectWebhooks
{
    public function handle(ProjectCreated $event): void
    {
        $webhooks = Webhook::where('active', true)
            ->where('user_id', $event->project->user_id)
            ->whereJsonContains('events', 'project.created')
            ->get();

        foreach ($webhooks as $webhook) {
            SendWebhookJob::dispatch($webhook, [
                'event' => 'project.created',
                'data'  => [
                    'id'         => $event->project->id,
                    'name'       => $event->project->name,
                    'created_at' => $event->project->created_at->toISOString(),
                ],
            ]);
        }
    }
}
```

Задание вебхука:

```php
<?php

namespace App\Jobs;

use App\Models\Webhook;
use App\Models\WebhookCall;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Http;

class SendWebhookJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $tries   = 3;
    public $backoff = [60, 300, 900]; // 1 min, 5 min, 15 min

    public function __construct(
        public Webhook $webhook,
        public array $payload
    ) {}

    public function handle(): void
    {
        $signature = hash_hmac('sha256', json_encode($this->payload), $this->webhook->secret);

        $response = Http::timeout(10)
            ->withHeaders([
                'X-Webhook-Signature' => $signature,
                'Content-Type'        => 'application/json',
            ])
            ->post($this->webhook->url, $this->payload);

        WebhookCall::create([
            'webhook_id'      => $this->webhook->id,
            'event'           => $this->payload['event'],
            'payload'         => $this->payload,
            'response_status' => $response->status(),
            'response_body'   => $response->body(),
            'attempt'         => $this->attempts(),
            'delivered_at'    => $response->successful() ? now() : null,
        ]);

        if (!$response->successful()) {
            throw new \Exception('Webhook delivery failed: ' . $response->status());
        }
    }
}
```

Это задание:

- Отправляет вебхук с заголовком подписи
- Записывает в лог каждую попытку
- Повторяет попытку с задержкой при неудаче
- Прекращает выполнение через 10 секунд

### Проверка подписи

Принимающий сервис должен проверить подпись:

```php
<?php

// На стороне получателя
$signature = $request->header('X-Webhook-Signature');
$payload   = $request->getContent();

$expectedSignature = hash_hmac('sha256', $payload, $secret);

if (!hash_equals($expectedSignature, $signature)) {
    return response()->json(['error' => 'Invalid signature'], 401);
}
```

Это предотвращает подделку вебхуков. Без проверки подписи кто угодно мог бы отправлять поддельные вебхуки на конечные точки ваших пользователей.

### Что вы изучаете

Вебхуки — это способ общения API. Этот проект учит вас, что не всё может происходить синхронно — некоторые операции нужно ставить в очередь. Вы изучаете повторные попытки заданий, стратегии задержек и обработку таймаутов.

Вы также узнаёте, что безопасность важна даже в коммуникации между машинами. Подписи гарантируют, что вебхуки подлинные.

Самое главное — вы узнаёте, что API нуждаются в наблюдаемости. Логирование попыток отправки вебхуков позволяет пользователям отлаживать проблемы интеграции. Хорошие API делают отладку простой.

## Проект 9: Публичный API с ограничением запросов - Управление доступом

Ключевые концепции: Ограничение скорости запросов, API-ключи, отслеживание использования, мидлвары, стратегии троттлинга

Публичные API нуждаются в защите от злоупотреблений. Вы не можете позволить одному клиенту обрушивать ваши серверы неограниченным количеством запросов. Этот проект учит вас, как реализовать продвинутое ограничение скорости запросов и отслеживание использования.

### Управление API-ключами

```php
<?php

Schema::create('api_keys', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('name');
    $table->string('key')->unique();
    $table->string('tier')->default('free'); // free, pro, enterprise
    $table->timestamp('last_used_at')->nullable();
    $table->boolean('active')->default(true);
    $table->timestamps();
});

Schema::create('api_key_usages', function (Blueprint $table) {
    $table->id();
    $table->foreignId('api_key_id')->constrained();
    $table->string('endpoint');
    $table->timestamp('requested_at');
    $table->integer('response_status');
    $table->integer('response_time_ms');

    $table->index(['api_key_id', 'requested_at']);
});
```

Генерируйте ключи безопасно:

```php
<?php

public function create(Request $request)
{
    $request->validate([
        'name' => ['required', 'string', 'max:255'],
    ]);

    $apiKey = $request->user()->apiKeys()->create([
        'name' => $request->name,
        'key'  => 'sk_' . bin2hex(random_bytes(32)),
        'tier' => 'free',
    ]);

    return response()->json([
        'key'     => $apiKey->key,
        'name'    => $apiKey->name,
        'message' => 'Store this key securely. It will not be shown again.',
    ], 201);
}
```

Показывайте ключ только один раз. Никогда не храните его в открытом виде, если можете хешировать (хотя для API-ключей открытый текст часто необходим для проверки).

### Мидлвар для ограничения скорости запросов

Встроенное ограничение скорости запросов в Laravel мощное:

```php
<?php

// В RouteServiceProvider
RateLimiter::for('api', function (Request $request) {
    $apiKey = ApiKey::where('key', $request->bearerToken())->first();

    if (!$apiKey) {
        return Limit::perMinute(10); // Неаутентифицированные: 10/мин
    }

    return match ($apiKey->tier) {
        'free'       => Limit::perMinute(60)->by($apiKey->id),
        'pro'        => Limit::perMinute(300)->by($apiKey->id),
        'enterprise' => Limit::none(),
    };
});
```

Примените его к маршрутам:

```php
<?php

Route::middleware('throttle:api')->group(function () {
    // Маршруты с ограничением скорости запросов
});
```

Laravel автоматически возвращает ответ `429 Too Many Requests` при превышении лимитов, включая заголовки `X-RateLimit-*`.

### Пользовательский мидлвар для API-ключей

```php
<?php

namespace App\Http\Middleware;

use App\Models\ApiKey;
use Closure;
use Illuminate\Http\Request;

class AuthenticateApiKey
{
    public function handle(Request $request, Closure $next)
    {
        $key = $request->bearerToken();

        if (!$key) {
            return response()->json([
                'error' => 'API key required'
            ], 401);
        }

        $apiKey = ApiKey::where('key', $key)
            ->where('active', true)
            ->first();

        if (!$apiKey) {
            return response()->json([
                'error' => 'Invalid API key'
            ], 401);
        }

        $apiKey->update(['last_used_at' => now()]);
        $request->merge(['api_key' => $apiKey]);

        return $next($request);
    }
}
```

### Отслеживание использования

Отслеживайте каждый запрос:

```php
<?php

namespace App\Http\Middleware;

use App\Models\ApiKeyUsage;
use Closure;
use Illuminate\Http\Request;

class TrackApiUsage
{
    public function handle(Request $request, Closure $next)
    {
        $startTime = microtime(true);
        $response  = $next($request);
        $duration  = (microtime(true) - $startTime) * 1000;

        if ($apiKey = $request->get('api_key')) {
            ApiKeyUsage::create([
                'api_key_id'       => $apiKey->id,
                'endpoint'         => $request->path(),
                'requested_at'     => now(),
                'response_status'  => $response->status(),
                'response_time_ms' => round($duration),
            ]);
        }

        return $response;
    }
}
```

Эти данные позволяют вам:

- Показывать пользователям их использование
- Выставлять счета на основе потребления
- Определять медленные конечные точки
- Обнаруживать паттерны злоупотреблений

### Конечная точка аналитики использования

```php
<?php

public function usage(Request $request)
{
    $apiKey = $request->get('api_key');

    $today = $apiKey->usages()
        ->whereDate('requested_at', today())
        ->count();

    $thisMonth = $apiKey->usages()
        ->whereMonth('requested_at', now()->month)
        ->count();

    $byEndpoint = $apiKey->usages()
        ->whereMonth('requested_at', now()->month)
        ->groupBy('endpoint')
        ->selectRaw('endpoint, COUNT(*) as count')
        ->orderByDesc('count')
        ->limit(10)
        ->get();

    return response()->json([
        'today'         => $today,
        'this_month'    => $thisMonth,
        'limit'         => $this->getLimitForTier($apiKey->tier),
        'top_endpoints' =>  $byEndpoint,
    ]);
}
```

### Что вы изучаете

Этот проект учит вас, что публичные API отличаются от API для аутентифицированных пользователей. Вам нужна другая аутентификация (API-ключи вместо сессий/токенов), другие стратегии ограничения скорости запросов и комплексное отслеживание использования.

Вы узнаёте, что ограничение скорости запросов — это не только предотвращение злоупотреблений, но и управление ресурсами и создание ценовых уровней. Вы также узнаёте, что наблюдаемость критически важна. Пользователям нужно видеть своё использование. Вам нужно видеть, как используется ваш API.

## Проект 10: Альтернатива GraphQL - Другая парадигма

Ключевые концепции: GraphQL с Lighthouse, проектирование схемы, предотвращение проблемы N+1 с помощью dataloaders, резолверы

GraphQL не лучше REST, но он решает другие проблемы. Этот проект учит вас альтернативной парадигме API и помогает понять, когда каждый подход имеет смысл.

### Настройка Lighthouse

```sh
composer require nuwave/lighthouse
php artisan vendor:publish --tag=lighthouse-schema
```

Lighthouse — это нативный для Laravel GraphQL. Он использует ваши модели Eloquent и следует соглашениям Laravel.

### Схема

GraphQL начинается со схемы, которая определяет весь ваш API:

```graphql
type Query {
  posts(first: Int! @paginate): [Post!]! @paginate
  post(id: ID! @eq): Post @find
  me: User @auth
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User! @belongsTo
  comments: [Comment!]! @hasMany
  created_at: DateTime!
  updated_at: DateTime!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]! @hasMany
}

type Comment {
  id: ID!
  content: String!
  post: Post! @belongsTo
  author: User! @belongsTo
  created_at: DateTime!
}
```

Эта схема определяет всё: типы, связи, запросы. Lighthouse использует директивы (такие как `@paginate`, `@hasMany`) для автоматической генерации резолверов на основе ваших моделей Eloquent.

### Автоматический CRUD с Eloquent

Поскольку Lighthouse понимает Laravel, вы получаете готовые запросы:

```graphql
query {
  posts(first: 10) {
    data {
      id
      title
      author {
        name
      }
      comments {
        content
        author {
          name
        }
      }
    }
  }
}
```

Lighthouse автоматически:

- Разбивает результаты на страницы
- Загружает связи заранее для предотвращения проблемы N+1
- Преобразует модели в соответствии со схемой
- Обрабатывает аутентификацию с помощью @auth

### Пользовательские резолверы

Для сложной логики пишите пользовательские резолверы:

```php
<?php

namespace App\GraphQL\Queries;

class PostsByTag
{
    public function __invoke($rootValue, array $args)
    {
        return Post::whereHas('tags', function ($query) use ($args) {
            $query->where('slug', $args['tag']);
        })->paginate($args['first']);
    }
}
```

Сошлитесь на него в вашей схеме:

```graphql
type Query {
  postsByTag(tag: String!, first: Int!): [Post!]!
    @paginate
    @field(resolver: "App\\GraphQL\\Queries\\PostsByTag")
}
```

### Мутации

Мутации GraphQL подобны операциям POST/PUT/DELETE в REST:

```graphql
type Mutation {
  createPost(input: CreatePostInput! @spread): Post
    @create
    @guard

  updatePost(id: ID!, input: UpdatePostInput! @spread): Post
    @update
    @guard

  deletePost(id: ID!): Post
    @delete
    @guard
}

input CreatePostInput {
  title: String! @rules(apply: ["required", "max:255"])
  content: String! @rules(apply: ["required"])
  category_id: ID!
}
```

Директива `@guard` требует аутентификации. Директива `@rules` применяет валидацию Laravel. Это паттерны Laravel в GraphQL.

### Когда GraphQL уместен

GraphQL решает проблему «избыточного» и «недостаточного» получения данных. В REST вам могут понадобиться несколько запросов:

```yaml
GET /api/posts/1
GET /api/posts/1/author
GET /api/posts/1/comments
GET /api/posts/1/comments/123/author
```

С GraphQL это один запрос, который сразу возвращает пост, его автора и комментарии в нужной структуре.

```graphql
query {
  post(id: 1) {
    title
    author { name }
    comments {
      content
      author { name }
    }
  }
}
```

Клиент запрашивает ровно то, что ему нужно. Ни больше, ни меньше.

Но у GraphQL есть и издержки:

- Более сложная реализация
- Труднее кэшировать (нет кэширования, основанного на URL)
- Сложно ограничивать «сложность» запросов
- REST проще для простых случаев

### Что вы изучаете

Этот проект учит вас, что REST — не единственный способ построения API. GraphQL предлагает другие компромиссы: больше гибкости для клиентов, больше сложности для серверов. Ни один из подходов не является универсально лучшим.

Вы узнаёте, что экосистема Laravel поддерживает несколько парадигм. Lighthouse показывает, что GraphQL может быть нативным для Laravel, используя те же модели, валидацию и паттерны, которые вы уже знаете.

## За пределами проектов

Эти десять проектов дают вам фундамент, но не являются исчерпывающими. Реальные продакшен-API требуют большего.

### Тестирование

Каждый эндпойнт нуждается в тестах. Используйте Pest или PHPUnit:

```php
<?php

test('authenticated users can create posts', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)->postJson('/api/posts', [
        'title'   => 'Test Post',
        'content' => 'Content here',
    ]);

    $response->assertCreated()
        ->assertJsonStructure(['data' => ['id', 'title', 'content']]);

    $this->assertDatabaseHas('posts', [
        'title'   => 'Test Post',
        'user_id' => $user->id,
    ]);
});
```

Тестирование API часто проще, чем тестирование полноценных full‑stack приложений, потому что вы проверяете только JSON‑ответы. Пишите тесты по мере разработки фич, а не постфактум.

### Документация

API бесполезен, если никто не знает, как им пользоваться. Для автоматической генерации документации можно использовать Scribe:

```sh
composer require --dev knuckleswtf/scribe
php artisan vendor:publish --tag=scribe-config
php artisan scribe:generate
```

Scribe читает ваши маршруты, контроллеры и `Form Request`‑классы и автоматически генерирует документацию. Добавляйте аннотации для большей ясности.

```php
<?php

/**
 * Create a new post
 *
 * Creates a new post for the authenticated user.
 *
 * @bodyParam title string required The post title. Example: My First Post
 * @bodyParam content string required The post content. Example: This is the content.
 *
 * @response 201 {"data":{"id":1,"title":"My First Post"}}
 */
public function store(StorePostRequest $request)
{
    // ...
}
```

Хорошую документацию так же важно иметь, как и хороший код.

### Версионирование

API нуждаются в версионировании. Ломающие изменения неизбежны. Не нарушайте работу существующих клиентов:

```php
<?php

Route::prefix('v1')->group(function () {
    // Маршруты версии 1
});

Route::prefix('v2')->group(function () {
    // Маршруты версии 2 с ломающими изменениями
});
```

Или используйте версионирование на основе заголовков. Оба подхода рабочие. Главное — быть последовательным.

### Обработка ошибок

Единообразные ответы об ошибках имеют значение:

```php
<?php

namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

class Handler extends ExceptionHandler
{
    public function render($request, Throwable $e)
    {
        if ($request->expectsJson()) {
            if ($e instanceof NotFoundHttpException) {
                return response()->json([
                    'message' => 'Resource not found'
                ], 404);
            }

            if ($e instanceof ValidationException) {
                return response()->json([
                    'message' => 'Validation failed',
                    'errors' => $e->errors()
                ], 422);
            }

            return response()->json([
                'message' => $e->getMessage()
            ], 500);
        }

        return parent::render($request, $e);
    }
}
```

Клиенты никогда не должны видеть HTML-страницы ошибок или стек-трейсы в продакшене.

### Мониторинг

Вам нужно знать, когда ваш API сломан. Используйте инструменты вроде Sentry или Bugsnag для отслеживания ошибок. В разработке используйте Laravel Telescope, чтобы видеть все запросы, задания и события.

Настройте конечные точки проверки состояния:

```php
<?php

Route::get('/health', function () {
    return response()->json([
        'status'    => 'healthy',
        'timestamp' => now()->toISOString(),
    ]);
});
```

Ваши инструменты мониторинга могут опрашивать этот эндпойнт, чтобы проверить, что ваш API отвечает.

## Реальное обучение происходит дальше

Вот правда: вы по-настоящему не изучаете эти концепции, просто читая о них. Вы их изучаете, строя их, совершая ошибки, рефакторя и строя заново.

Выберите один проект из списка. Не берите самый сложный, чтобы что-то доказать. Выберите тот, который кажется интересным. Постройте его полностью: тесты, документация, обработка ошибок — всё. Разверните его куда-нибудь. Пусть поработает неделю. Затем вернитесь и переделайте его с учётом полученного опыта.

Затем возьмите следующий проект.

Цель не в том, чтобы собрать готовые проекты в GitHub-репозитории. Цель — усвоить паттерны, которые делают API на Laravel поддерживаемыми. Вы хотите достичь уровня, когда вы не думаете, использовать ли ресурс API — вы просто используете его. Когда ограничение скорости запросов не добавляется потом — оно есть с самого начала.

На это нужно время. Нужна практика. Нужно строить одни и те же паттерны достаточно много раз, чтобы они стали автоматическими.

Эти проекты дают вам структуру. А обучение? Оно происходит только когда вы пишете код.


---

Оригинальная статья: [API-First Laravel Projects](https://www.juststeveking.com/articles/api-first-laravel-projects/) (English)
