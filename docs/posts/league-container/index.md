---
title: 'League Container'
description: 'Перевод документации пакета league/container'
slug: league-container
date: 2024-06-08
tags:
  - PSR-11
  - контейнер
  - ООП
---

Познакомимся с основами использования сервисного контейнера PSR-11 на примере `league/container` от группы The League of Extraordinary Packages.

<!-- more -->

## Введение

Класс `League\Container\Container` (далее — `Container`) — это контейнер для внедрения зависимостей. Он позволяет вам реализовать соответствующий паттерн проектирования, что означает, что вы можете отделить зависимости вашего класса и позволить контейнеру внедрять их там, где они нужны.

- Простой API.
- Взаимозаменяемость. `Container` является реализацией [PSR-11](https://www.php-fig.org/psr/psr-11/).
- Скорость. Благодаря своей простоте `Container` очень быстр.
- Сервис-провайдеры позволяют упаковывать код или конфигурацию для пакетов, которые вы регулярно используете.
- Инфлекторы позволяют манипулировать объектами, разрешаемыми через контейнер, на основе их типа.

```php
<?php declare(strict_types=1);

namespace Acme;

class Foo
{
    public Bar $bar;

    public function __construct()
    {
        $this->bar = new Bar;
    }
}

class Bar {}
```

В коде выше класс `Acme\Foo` имеет зависимость от `Acme\Bar`. Это тесно связанная зависимость, что означает, что каждый раз, когда создается экземпляр `Acme\Foo`, он самостоятельно создает также экземпляр `Acme\Bar`.

С помощью рефакторинга, чтобы класс принимал его зависимость в качестве аргумента конструктора, мы можем ослабить эту зависимость:

```php
<?php declare(strict_types=1);

namespace Acme;

class Foo
{
    public Bar $bar;

    public function __construct(Bar $bar)
    {
        $this->bar = $bar;
    }
}

class Bar {}
```

Во внедрении зависимостей нет ничего сложного, и контейнер позволяет реализовать его в ваших приложениях.

## Установка

```bash
composer require league/container
```

## Использование

Контейнер позволяет регистрировать сервисы с их зависимостями или без них для последующего извлечения. Это своего рода реестр, который при правильном использовании позволяет реализовать паттерн проектирования Dependency Injection.

На примере нашего введения мы можем начать разбираться с тем, как работает контейнер. Теперь, когда `Acme\Foo` принимает `Acme\Bar` в качестве аргумента конструктора, мы можем использовать контейнер для его настройки.

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Foo::class)->addArgument(Acme\Bar::class);
$container->add(Acme\Bar::class);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);      // true
var_dump($foo->bar instanceof Acme\Bar); // true
```

В приведённом выше примере мы зарегистрировали `Acme\Foo` и `Acme\Bar` в контейнере, а также сообщили контейнеру, что при запросе `Acme\Foo` мы хотим получить его с аргументом `Acme\Bar`.

Когда мы обращаемся к контейнеру через `get(Acme\Foo::class)`, он знает, что сначала нужно получить `Acme\Bar` и ввести его в качестве аргумента конструктора при инстанцировании `Acme\Foo`.

### Псевдонимы

Мы можем внести небольшие изменения в приведённый выше код, чтобы использовать псевдонимы для указания на реальный класс:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add('foo', Acme\Foo::class)->addArgument(Acme\Bar::class);
$container->add('bar', Acme\Bar::class);

$foo = $container->get('foo');

var_dump($foo instanceof Acme\Foo);      // true
var_dump($foo->bar instanceof Acme\Bar); // true
```

Это полезно, особенно если речь идет не о конкретике, а об интерфейсах. Мы можем отрефакторить наш исходный пример, чтобы он зависел от интерфейса, и настроить контейнер на внедрение конкретной реализации:

```php
<?php declare(strict_types=1);

namespace Acme;

class Foo
{
    public BarInterface $bar;

    public function __construct(BarInterface $bar)
    {
        $this->bar = $bar;
    }
}

interface BarInterface {}
class BarA implements BarInterface {}
class BarB implements BarInterface {}
```

Теперь у нас есть `Acme\Foo`, зависящий от реализации `Acme\BarInterface` (`Acme\BarA`или `Acme\BarB`):

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

// Acme\Foo добавляется как обычно, но с аргументом Acme\BarInterface
$container->add(Acme\Foo::class)->addArgument(Acme\BarInterface::class);
// Acme\BarInterface добавлен как псевдоним, а Acme\BarA - как конкретная реализация,
// которую при необходимости можно легко поменять на Acme\BarB
$container->add(Acme\BarInterface::class, Acme\BarA::class);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);               // true
var_dump($foo->bar instanceof Acme\BarInterface); // true
var_dump($foo->bar instanceof Acme\BarA);         // true
var_dump($foo->bar instanceof Acme\BarB);         // false
```

`Container` имеет множество других возможностей и способов настройки для реализации внедрения зависимостей.

## Внедрение зависимостей

`Container` по своей сути представляет собой простой контейнер для внедрения зависимостей. В этом разделе основное внимание будет уделено тому, как реализовать различные типы внедрения зависимостей с помощью контейнера.

### Внедрение через конструктор

Передача зависимостей конструктору класса — это самый простой способ внедрения зависимостей. Когда ваши классы определены с помощью `Container`, он может легко соединить их вместе с помощью этого метода.

В качестве базового примера предположим, что у нас есть класс контроллера, который зависит от модели, и эта модель зависит от `PDO` для подключений к базе данных:

```php
<?php declare(strict_types=1);

namespace Acme;

class Controller
{
    public Model $model;

    public function __construct(Model $model)
    {
        $this->model = $model;
    }
}

class Model
{
    public PDO $pdo;

    public function __construct(PDO $pdo)
    {
        $this->pdo = $pdo;
    }
}
```

Это дерево зависимостей можно определить в контейнере, тогда всякий раз при получении `Acme\Controller` контейнер будет рекурсивно создавать все зависимости и внедрять их по мере необходимости:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Controller::class)->addArgument(Acme\Model::class);
$container->add(Acme\Model::class)->addArgument(PDO::class);

$container
    ->add(PDO::class)
    ->addArgument('dsn_string')
    ->addArgument('username')
    ->addArgument('password')
    ->addArgument([/* options */])
;

$controller = $container->get(Acme\Controller::class);

var_dump($controller instanceof Acme\Controller);   // true
var_dump($controller->model instanceof Acme\Model); // true
var_dump($controller->model->pdo instanceof PDO);   // true
```

### Внедрение через метод

Внедрение зависимостей также может быть достигнуто путём вызова и передачи зависимостей методам. Мы можем реорганизовать приведённый выше пример, чтобы модель получала `PDO` через сеттер вместо аргумента конструктора:

```php
<?php declare(strict_types=1);

namespace Acme;

class Controller
{
    public Model $model;

    public function __construct(Model $model)
    {
        $this->model = $model;
    }
}

class Model
{
    public \PDO $pdo;

    public function setPdo(\PDO $pdo)
    {
        $this->pdo = $pdo;
    }
}
```

Теперь нам нужно внести небольшое изменение в наше определение в контейнере, чтобы убедиться, что метод правильно вызывается при инстанцировании:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Controller::class)->addArgument(Acme\Model::class);

$container
    ->add(Acme\Model::class)
    // первый аргумент - имя вызываемого метода,
    // второй аргумент - массив аргументов для передачи в метод,
    // Container попытается разрешить каждый элемент массива через себя
    ->addMethodCall('setPdo', [PDO::class])
;

$container
    ->add(PDO::class)
    ->addArgument('dsn_string')
    ->addArgument('username')
    ->addArgument('password')
    ->addArgument([/* options */])
;

$controller = $container->get(Acme\Controller::class);

var_dump($controller instanceof Acme\Controller);   // true
var_dump($controller->model instanceof Acme\Model); // true
var_dump($controller->model->pdo instanceof PDO);   // true
```

### Фабрики

Контейнер может принимать любой вызываемый объект, который будет использоваться в качестве фабрики для разрешения ваших классов. Это наиболее эффективный способ разрешения ваших объектов, поскольку проверка определения не требуется, однако это снижает степень гибкости, которой вы можете воспользоваться.

Используя тот же пример, что и выше, мы можем определить его в `Container` следующим образом:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Controller::class, function () {
    $pdo   = new PDO('dsn_string', 'username', 'password', [/* options */]);
    $model = new Acme\Model;

    $model->setPdo($pdo);

    return new Acme\Controller($model);
});

$controller = $container->get(Acme\Controller::class);

var_dump($controller instanceof Acme\Controller);   // true
var_dump($controller->model instanceof Acme\Model); // true
var_dump($controller->model->pdo instanceof PDO);   // true
```

## Определения

Определения — это то, как `Container` внутренне описывает вашу карту зависимостей. Каждое определение содержит информацию о том, как создавать свои классы.

Как правило, `Container` сделает всё необходимое для создания определения за вас. Когда вы вызываете метод `add`, создаётся и возвращается определение, то есть любое дальнейшее взаимодействие происходит с определением, а не с контейнером:

```php
<?php declare(strict_types=1);

$container  = new League\Container\Container();
$definition = $container->add(Acme\Foo::class);

var_dump($definition instanceof League\Container\Definition\Definition); // true
```

При необходимости вы также можете расширить определение:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Foo::class);

// ... ещё немного кода

$container->extend(Acme\Foo::class)->addArgument(Acme\Bar::class);
$container->add(Acme\Bar::class);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);      // true
var_dump($foo->bar instanceof Acme\Bar); // true
```

Также возможно создание определений вручную и передача их в контейнер:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$fooDefinition = (new Definition(Acme\Foo::class))->addArgument(Acme\Bar::class);
$barDefinition = (new Definition(Acme\Bar::class));

$container->add($fooDefinition->getAlias(), $fooDefinition);
$container->add($barDefinition->getAlias(), $barDefinition);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);      // true
var_dump($foo->bar instanceof Acme\Bar); // true
```

### Агрегат

Контейнер использует агрегат для хранения всех определений. Это означает, что вы можете сначала создать свой агрегат, а затем передать его контейнеру:

```php
<?php declare(strict_types=1);

$definitions = [
    (new Definition(Acme\Foo::class))->addArgument(Acme\Bar::class),
    (new Definition(Acme\Bar::class)),
];

$aggregate = new League\Container\Definition\DefinitionAggregate($definitions);
$container = new League\Container\Container($aggregate);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);      // true
var_dump($foo->bar instanceof Acme\Bar); // true
```

Интерфейсы предоставляются для определений, а агрегаты означают, что вы можете создавать свои собственные реализации и передавать их контейнеру, как описано выше, если вам нужно больше или меньше функциональности, определённой для вашей карты зависимостей.

### Характеристики

Определения предоставляют несколько методов для указания желаемого поведения при разрешении объекта, который вы определяете. Все эти методы можно объединить в цепочку.

#### Добавление аргументов конструктора

Добавление аргумента в определение передаст этот аргумент конструктору определяемого класса при инстанцировании, а многократное обращение к этому конструктору передаст больше аргументов в том порядке, в котором они были добавлены:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container
    ->add(Acme\Foo::class)
    ->addArgument(Acme\Bar::class)
    ->addArgument(Acme\Baz::class)
;
```

У нас также есть прокси-метод для передачи нескольких аргументов за один вызов:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Foo::class)->addArguments([
    Acme\Bar::class,
    Acme\Baz::class,
]);
```

### Добавление вызовов методов

Мы можем определить один или несколько вызовов методов и аргументы, которые будут переданы им, эти аргументы будут разрешены через контейнер. (Один и тот же вызов метода может быть добавлен несколько раз для нескольких вызовов с одинаковыми или разными аргументами).

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container
    ->add(Acme\Foo::class)
    ->addMethodCall('setBar', [Acme\Bar::class])
    ->addMethodCall('setBaz', [Acme\Baz::class])
;
```

У нас также есть удобный метод, позволяющий добавить в определение несколько вызовов методов одновременно:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container
    ->add(Acme\Foo::class)
    ->addMethodCalls([
        ['setBar', [Acme\Bar::class]],
        ['setBaz', [Acme\Baz::class]],
    ])
;
```

### Определение общих объектов

Мы можем указать определению, что оно должно разрешаться только один раз и возвращать один и тот же экземпляр при каждом разрешении:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container
    ->add(Acme\Foo::class)
    ->setShared()
;
```

У нас также есть короткий метод, позволяющий сделать это одним вызовом метода:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->addShared(Acme\Foo::class);
```

Если вы хотите, чтобы все ваши определения по умолчанию были общими, вы можете определить это в контейнере, что означает, что метод `add` будет по умолчанию устанавливать ваши определения как общие, и несколько вызовов `get` будут возвращать один и тот же экземпляр. Только определения, сделанные после установки этого параметра, будут по умолчанию общими:

```php
<?php declare(strict_types=1);

$container = (new League\Container\Container())->defaultToShared();

$container->add(Acme\Foo::class);
```

Когда контейнер настроен на то, чтобы все определения по умолчанию были общими, мы можем специально определить определение как не общее:

```php
<?php declare(strict_types=1);

$container = (new League\Container\Container())->defaultToShared();

$container->add(Acme\Foo::class, Acme\Foo::class)->setShared(false);
```

Если у нас есть определение, помеченное как общее, и мы хотим принудительно получить новый экземпляр, мы можем вызвать метод `getNew`:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container
    ->add(Acme\Foo::class)
    ->setShared()
;

$container->getNew(Acme\Foo::class);
```

### Тегированные определения

Мы можем помечать определения тегами, и при получении псевдонима, заданного тегу, все определения, использующие этот тег, будут отображаться в индексированном массиве. К каждому определению можно добавить несколько тегов:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Foo::class)->addTag('foos');
$container->add(Acme\FooBar::class)->addTag('foos')->addTag('bars');
$container->add(Acme\Bar::class)->addTag('bars');

$foos = $container->get('foos'); // [Foo, FooBar]
$bars = $container->get('bars'); // [FooBar, Bar]
```

## Типы аргументов

Вы можете определить аргументы как определённые типы, известные контейнеру, чтобы он знал, что делать с этими значениями, без выполнения дальнейших проверок. Это дает выигрыш в производительности, поскольку при обнаружении одного из этих типов определений значение либо возвращается мгновенно, либо выполняется дальнейшее разрешение на основе заданного типа.

### Разрешаемые аргументы

Разрешаемые аргументы, по сути, являются внутренними аргументами по умолчанию для контейнера. Контейнер будет пытаться «разрулить» любой переданный ему аргумент, пока не получит значение, которое невозможно «разрулить» дальше.

Там, где это становится полезным для явного определения (например, при использовании вложенных псевдонимов), вы можете указать контейнеру, что при обнаружении аргумента он должен явно попытаться дополнительно «разрулить» это значение:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();
$container->add('alias1', new League\Container\Argument\ResolvableArgument('alias2'));
$container->add('alias2', Acme\Foo::class);

$foo = $container->get('alias1');

var_dump($foo instanceof Acme\Foo); // true
```

### Литеральные аргументы

Литеральные аргументы действуют противоположно разрешаемым аргументам: когда контейнер встречает один из них, он просто возвращает связанное значение без дальнейшего разрешения.

Какую проблему это решает? В основном контейнер ориентирован на производительность, однако он будет пытаться принять нежелательное решение для некоторых типов аргументов.

#### String

По умолчанию контейнер исчерпает все возможные параметры, прежде чем вернуть строку.

- Является ли строка псевдонимом чего-то ещё в контейнере?
- Является ли строка классом, экземпляр которого необходимо создать?
- Является ли строка в конечном итоге вызываемой и, следовательно, следует ли её рассматривать как фабрику?

Вы можете заставить контейнер обрабатывать строку как литерал, определив это поведение:

```php
<?php declare(strict_types=1);

use League\Container\Argument\Literal;

$container = new League\Container\Container();
$container->add('alias1', new Literal\StringArgument('alias2'));
$container->add('alias2', Acme\Foo::class);

$foo = $container->get('alias1');

var_dump($foo instanceof Acme\Foo); // false
var_dump($foo === 'alias2'); // true
```

#### Array

Подобно строке, контейнер попытается определить, является ли переданное значение массивом. Вы можете избежать этих проверок, определив массив как литерал:

```php
<?php declare(strict_types=1);

use League\Container\Argument\Literal;

$container = new League\Container\Container();
$container->add('an-array', new Literal\ArrayArgument(['blah', 'blah2']));

$arr = $container->get('an-array');

var_dump($arr === ['blah', 'blah2']); // true
```

#### Object и Callable

Контейнер хочет рассматривать любой вызываемый объект как фабрику, поэтому вместо того, чтобы возвращать ваш объект, замыкание и т. д., он будет вызывать его и возвращать результат.

Предположим, у вас есть объект, реализующий магический метод `__invoke`, но вы не хотите, чтобы контейнер фактически вызывал вызываемый объект. Для этого просто верните объект, переданный в качестве аргумента:

```php
<?php declare(strict_types=1);

namespace Acme;

class MyClass
{
    public function __invoke()
    {
        return 'hello';
    }
}
```

```php
<?php declare(strict_types=1);

use League\Container\Argument\Literal;

$container = new League\Container\Container();
$container->add('object', new Acme\MyClass());
// используем Literal\ObjectArgument или Literal\CallableArgument
$container->add('literal-object', new Literal\ObjectArgument(new Acme\MyClass()));

$obj = $container->get('object');

var_dump($obj instanceof Acme\MyClass); // false
var_dump($obj === 'hello'); // true

$literalObj = $container->get('literal-object');

var_dump($literalObj instanceof Acme\MyClass); // true
var_dump($literalObj === 'hello'); // false
```

Аналогично, если вы хотите передать какой-либо вызываемый объект в качестве аргумента, контейнер будет рассматривать его как фабрику и разрешать его. Вы можете избежать этого, определив его в качестве литерала:

```php
<?php declare(strict_types=1);

use League\Container\Argument\Literal;

$callback = function () {
    return 'hello';
};

$container = new League\Container\Container();
$container->add('callable', $callback);
$container->add('literal-callable', new Literal\CallableArgument($callback));

$cb = $container->get('callable');

var_dump($cb === $callback); // false
var_dump($cb === 'hello'); // true

$literalCb = $container->get('literal-callable');

var_dump($literalCb === $callback); // true
var_dump($literalCb === 'hello'); // false
```

#### Boolean, Integer и Float

Они не имеют никакого эффекта и существуют только для ясности и читаемости вашего кода с небольшой проверкой типов.

#### Все литеральные аргументы

Все литеральные классы аргументов являются удобными подклассами `League\Container\Argument\LiteralArgument`:

- `League\Container\Argument\Literal\ArrayArgument`
- `League\Container\Argument\Literal\BooleanArgument`
- `League\Container\Argument\Literal\CallableArgument`
- `League\Container\Argument\Literal\FloatArgument`
- `League\Container\Argument\Literal\IntegerArgument`
- `League\Container\Argument\Literal\ObjectArgument`
- `League\Container\Argument\Literal\StringArgument`

## Сервис-провайдеры

Сервис-провайдеры (они же — _поставщики услуг_) дают преимущества в организации определений контейнеров, а также повышают производительность более крупных приложений, поскольку определения, зарегистрированные в сервис-провайдере, лениво регистрируются в момент получения сервиса.

Для создания сервис-провайдера вам необходимо расширить базовый класс `AbstractServiceProvider`, предоставив методы `register` и `provides`, который будет возвращать `true` или `false`, когда контейнер вызывает его с именем сервиса (это позволяет контейнеру заранее знать, что предоставляет сервис-провайдер, для отложенной загрузки):

```php
<?php declare(strict_types=1);

namespace Acme\ServiceProvider;

use League\Container\ServiceProvider\AbstractServiceProvider;

class SomeServiceProvider extends AbstractServiceProvider
{
    /**
     * Метод provides - это способ сообщить контейнеру,
     * что сервис предоставляется этим сервис-провайдером.
     * К каждому сервису, зарегистрированному через
     * этот сервис-провайдер, должен быть добавлен псевдоним
     * в массив $services, иначе он будет проигнорирован.
     */
    public function provides(string $id): bool
    {
        $services = [
            'key',
            Some\Controller::class,
            Some\Model::class,
            Some\Request::class,
        ];

        return in_array($id, $services);
    }

    /**
     * С помощью метода register вы определяете сервисы
     * таким же образом, как и в случае с контейнером.
     * Это удобный способ получения данных, если контейнер предоставлен, вы
     * можете вызвать любой из методов, которые вы использовали бы при определении
     * сервисов напрямую, но помните, что любой псевдоним, добавленный в контейнер
     * здесь, при передаче в метод `provides` должен возвращать значение true,
     * иначе он будет проигнорирован контейнером.
     */
    public function register(): void
    {
        $this->getContainer()->add('key', 'value');

        $this->getContainer()
            ->add(Some\Controller::class)
             ->addArgument(Some\Request::class)
             ->addArgument(Some\Model::class)
        ;

        $this->getContainer()->add(Some\Request::class);
        $this->getContainer()->add(Some\Model::class);
    }
}
```

Чтобы зарегистрировать этот сервис-провайдер в контейнере, просто передайте экземпляр вашего провайдера в метод `League\Container\Container::addServiceProvider`:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->addServiceProvider(new Acme\ServiceProvider\SomeServiceProvider);
```

Метод `register` не вызывается до тех пор, пока контейнер не запросит один из предоставляемых им псевдонимов, поэтому, когда мы хотим получить один из элементов, предоставленных сервис-провайдером, он фактически не будет зарегистрирован до тех пор, пока в нём не возникнет необходимость. Это повышает производительность для более крупных приложений, поскольку ваша карта зависимостей растёт.

### Загружаемые сервис-провайдеры

Если есть функциональность, которую необходимо запустить при добавлении сервис-провайдера в контейнер, например, настройка инфлекторов, включение конфигурационных файлов и т. д., мы можем сделать сервис-провайдер загружаемым, внедрив интерфейс `League\Container\ServiceProvider\BootableServiceProviderInterface`:

```php
<?php declare(strict_types=1);

namespace Acme\ServiceProvider;

use League\Container\ServiceProvider\AbstractServiceProvider;
use League\Container\ServiceProvider\BootableServiceProviderInterface;

class SomeServiceProvider extends AbstractServiceProvider implements BootableServiceProviderInterface
{
    /**
     * Точно так же этот метод имеет доступ к самому контейнеру
     * и может взаимодействовать с ним как угодно, с той лишь разницей,
     * что метод boot вызывается сразу после регистрации сервис-провайдера
     * в контейнере, а это значит, что всё в этом методе загружается с нетерпением.
     *
     * Если вы хотите применить инфлекторы или зарегистрировать другие
     * сервис-провайдеры, кроме этого, они должны быть из загружаемого
     * сервис-провайдера, такого как этот, иначе будут проигнорированы.
     */
    public function boot(): void
    {
        $this->getContainer()
             ->inflector('SomeType')
             ->invokeMethod('someMethod', ['some_arg'])
         ;
    }

    public function provides(string $id): bool
    {
        // ...
    }

    public function register(): void
    {
        // ...
    }
}
```

## Инфлекторы

Инфлекторы позволяют определить манипуляции с объектом определённого типа как последний шаг перед его возвратом контейнером.

Это удобно, например, когда вы хотите вызвать метод для всех объектов, реализующих определённый интерфейс.

Представьте, что у вас есть интерфейс `LoggerAwareInterface`, и вы хотите вызывать метод `setLogger`, передавая в него логгер каждый раз, когда извлекается класс, реализующий этот интерфейс:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

$container->add(Acme\Logger::class);
$container->add(Acme\LoggerAwareClass::class); // реализует LoggerAwareInterface
$container->add(Acme\Other\LoggerAwareClass::class); // реализует LoggerAwareInterface

$container
    ->inflector(LoggerAwareInterface::class)
    ->invokeMethod('setLogger', [Acme\Logger::class]) // Acme\Logger будет разрешаться через контейнер
;

```

Теперь вместо того, чтобы добавлять вызов метода в каждый класс по отдельности, мы можем просто определить инфлектор, который будет вызывать метод для каждого класса данного типа.

## Контейнеры-делегаты

Контейнеры-делегаты — это способ регистрации одного или нескольких резервных контейнеров, которые будут использоваться для попыток разрешения сервисов, когда они не могут быть разрешены с помощью данного контейнера.

Делегат должен быть реализацией PSR-11 и может быть зарегистрирован с помощью метода `delegate`:

```php
<?php declare(strict_types=1);

namespace Acme\Container;

use Psr\Container\ContainerInterface;

class DelegateContainer implements ContainerInterface
{
    // ..
}
```

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();
$delegate  = new Acme\Container\DelegateContainer();

// этот метод может быть вызван несколько раз, каждый делегат
// проверяется в том порядке, в котором он был зарегистрирован
$container->delegate($delegate);
```

Теперь, когда делегат зарегистрирован, если сервис не может быть разрешён через основной контейнер, он будет использовать методы `has` и `get` делегата для разрешения запрашиваемого сервиса.

## Автовнедрение

!!! note "Примечание"

    Автовнедрение по умолчанию отключено, но его можно включить, зарегистрировав `ReflectionContainer` в качестве контейнера-делегата. Читайте ниже и ознакомьтесь с [документацией по контейнерам-делегатам](#konteinery-delegaty).

`Container` способен автоматически разрешать ваши объекты и все их зависимости рекурсивно, проверяя подсказки типов аргументов конструктора. К сожалению, у этого способа разрешения есть несколько небольших ограничений, но он отлично подходит для небольших приложений. Во-первых, вы ограничены внедрениями конструктора, а во-вторых, все внедрения должны быть объектами.

Рассмотрим приведённый ниже код:

```php
<?php declare(strict_types=1);

namespace Acme;

class Foo
{
    public Bar $bar;

    public Baz $baz;

    public function __construct(Bar $bar, Baz $baz)
    {
        $this->bar = $bar;
        $this->baz = $baz;
    }
}

class Bar
{
    public Bam $bam;

    public function __construct(Bam $bam)
    {
        $this->bam = $bam;
    }
}

class Baz
{
    // ..
}

class Bam
{
    // ..
}
```

`Acme\Foo` имеет 2 зависимости: `Acme\Bar` и `Acme\Baz`, `Acme\Bar` имеет дополнительную зависимость `Acme\Bam`. Обычно, чтобы вернуть полностью настроенный экземпляр `Acme\Foo`, нужно сделать следующее:

```php
<?php declare(strict_types=1);

$bam = new Acme\Bam();
$baz = new Acme\Baz();
$bar = new Acme\Bar($bam);
$foo = new Acme\Foo($bar, $baz);
```

При наличии вложенных зависимостей это может стать довольно громоздким и сложным для отслеживания. С помощью контейнера вернуть полностью сконфигурированный экземпляр `Acme\Foo` можно просто запросив `Acme\Foo` из контейнера:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

// регистрируем ReflectionContainer в качестве делегата, чтобы включить автоматическое внедрение
$container->delegate(
    new League\Container\ReflectionContainer()
);

$foo = $container->get(Acme\Foo::class);

var_dump($foo instanceof Acme\Foo);           // true
var_dump($foo->bar instanceof Acme\Bar);      // true
var_dump($foo->baz instanceof Acme\Baz);      // true
var_dump($foo->bar->bam instanceof Acme\Bam); // true
```

!!! note "Примечание"

    ReflectionContainer по умолчанию будет разрешать то, что вы запрашиваете, каждый раз, когда вы это запрашиваете.

Если вы хотите, чтобы ReflectionContainer кэшировал разрешения и брал их из этого кэша, если они доступны, вы можете включить эту функцию, как показано ниже:

```php
<?php declare(strict_types=1);

$container = new League\Container\Container();

// регистрируем ReflectionContainer в качестве делегата, чтобы включить автоматическое внедрение
$container->delegate(
    new League\Container\ReflectionContainer(true)
);

$fooOne = $container->get(Acme\Foo::class);
$fooTwo = $container->get(Acme\Foo::class);

var_dump($fooOne === $fooTwo); // true
```

## Заключение

Если вам пригодилась эта статья и вы хотите почитать ещё что-нибудь на эту тему, поддержите сайт необременительной для вас суммой, указав в комментарии свои пожелания для одной из будущих статей.

---

[Оригинальная документация](https://container.thephpleague.com/4.x/) (English)
