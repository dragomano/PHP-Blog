---
title: 'SOLID для чайников'
description: 'Памятка по принципам SOLID на примере PHP.'
slug: solid-dlya-chajnikov
date: 2021-04-01
tags:
  - ООП
---

В этой статье рассмотрим определения и суть принципов SOLID.

<!-- more -->

## S — Single Responsibility Principle (Принцип единственной ответственности), SRP

> Не берись за чужую работу.

У класса должен быть только один мотив для изменения.

Класс должен делать только одно определённое действие.

Это не означает, что класс должен содержать только один метод, выполняющий одно конкретное действие (хотя так проще всего добиться соблюдения этого принципа) — достаточно лишь того, чтобы класс был посвящен работе с одной конкретной сущностью. Например, класс _Category_ для работы только с категориями (но не для обработки страниц, тегов и прочего). И чем реже вы будете в дальнейшем менять что-либо в этом классе, тем лучше.

Иными словами, вместо методов `showCategory`, `showPage` и `showTag` в одном классе лучше создать по одному классу для каждой сущности:

```php
<?php

class Category
{
    public function show(int $id)
    {
        /* отображаем категорию */
    }
}
```

```php
<?php

class Page
{
    public function show(int $id)
    {
        /* отображаем страницу */
    }
}
```

```php
<?php

class Tag
{
    public function show(int $id)
    {
        /* отображаем тег */
    }
}
```

### Что ещё почитать?

* [Принцип единственной ответственности](https://laravel.su/library/solid#princip-edinstvennoi-otvetstvennosti)
* [Один класс — одна задача](https://laravel.su/library/actions)

## O — Open-Closed Principle (Принцип открытости-закрытости), OCP

> Не меняй то, что работает.

Класс должен быть открыт для расширения, но закрыт для изменений.

Пример:

```php
<?php

class First
{
    final public method1()
    {
    }

    final public method2()
    {
    }
}
```

Добавляем новый метод, не меняя (но расширяя!) базовый класс:

```php
<?php

class Second extends First
{
    final public method3()
    {
    }
}
```

### Что ещё почитать?

* [Принцип открытости/закрытости](https://laravel.su/library/solid#princip-otkrytostizakrytosti)

## L — Liskov Substitution Principle (Принцип подстановки Лисков), LSP

> Рождённый ползать летать не может.

Подклассы должны дополнять, а не замещать поведение базового класса.

Предположим, у нас есть базовый класс `Bird` и подклассы `Sparrow` и `Penguin`:

```php
<?php

class Bird
{
    public function fly()
    {
        return "Я умею летать!";
    }
}

class Sparrow extends Bird
{
    // Воробей может летать
}

class Penguin extends Bird
{
    public function fly()
    {
        throw new Exception("Я не умею летать!");
    }
}
```

В этом примере `Sparrow` корректно наследует поведение `Bird`, но `Penguin` нарушает принцип подстановки Лисков, так как он не умеет летать. Если мы заменим объект `Bird` на `Penguin`, это приведёт к ошибке.

Чтобы избежать этого, мы можем использовать интерфейсы или абстрактные классы:

```php
<?php

interface Flyable
{
    public function fly();
}

class Sparrow implements Flyable
{
    public function fly()
    {
        return "Я умею летать!";
    }
}

class Penguin
{
    // Пингвины не реализуют интерфейс Flyable
}
```

Теперь, если у нас есть функция, которая принимает `Flyable`, она будет работать только с классами, которые могут летать, и не будет пытаться использовать `Penguin`, что соответствует принципу подстановки Лисков.

### Что ещё почитать?

* [Принцип подстановки Барбары Лисков](https://laravel.su/library/solid#princip-podstanovki-barbary-liskov)

## I — Interface Segregation Principle (Принцип разделения интерфейсов), ISP

> Лучше меньше, да лучше.

Клиенты не должны зависеть от неиспользуемых ими методов.

Лучше использовать несколько небольших интерфейсов с используемыми методами, чем один большой с кучей методов, которые необходимо реализовывать, даже если вам они не нужны.

Неправильно:

```php
<?php

class Example implements OneMegaBigInterface {}
```

Правильно:

```php
<?php

class Example implements FirstInterface, SecondInterface, ThirdInterface {}
```

### Что ещё почитать?

* [Чистый код: Принцип разделения интерфейсов (Interface Segregation Principle)](https://iv-vi.dev/article/base/oop/chistyy-kod-princip-razdeleniya-interfeysov-solid)
* [Принцип разделения интерфейса](https://laravel.su/library/solid#princip-razdeleniia-interfeisa)

## D — Dependency Inversion Principle (Принцип инверсии зависимостей), DIP

> Сначала подумай, потом делай.

Модули верхних уровней не должны импортировать сущности из модулей нижних уровней. Оба типа модулей должны зависеть от абстракций.

Абстракции не должны зависеть от деталей. Детали должны зависеть от абстракций.

Ослабляйте связи с помощью внедрения зависимостей через конструктор, свойства или методы.

Неправильно (класс A жёстко связан с классом B):

```php
<?php

class A
{
    public function handle()
    {
        $this->something = new B();
    }
}
```

Правильно:

```php
<?php

class A
{
    private B $something;

    public function __construct(B $b)
    {
        $this->something = $b;
    }

    public function handle()
    {
        $this->something->doSomething();
    }
}

$test = new A(new B());
$test->handle();
```

И так тоже правильно:

```php
<?php

class A
{
    public function handle(B $b)
    {
        $b->doSomething();
    }
}

$test = new A();
$test->handle(new B());
```

### Что ещё почитать?

* [Принцип инверсии зависимостей](https://laravel.su/library/solid#princip-inversii-zavisimostei)
