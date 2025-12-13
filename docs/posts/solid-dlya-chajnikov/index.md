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

??? info "Сказка о Бобре-строителе"

    Жил-был Бобёр, который решил, что будет делать вообще всё: и плотины строить, и рыбу ловить, и обед готовить, и в домике убираться, и бобрят математике учить. В какой‑то момент он так вымотался, что перестал успевать хоть что‑то делать нормально. Плотины текли, рыба уплывала, а бобрята только путались в задачках.

    Тогда мудрая Сова сказала: «Делай то, что у тебя получается лучше всего — строй плотины. А с остальным пусть помогают друзья».

    Плохо (Бобёр делает всё сам):

    ```php
    <?php

    class Бобёр
    {
        public function строитьПлотину()
        {
            echo "Строю плотину\n";
        }

        public function ловитьРыбу()
        {
            echo "Ловлю рыбу\n";
        }

        public function готовитьЕду()
        {
            echo "Готовлю еду\n";
        }

        public function учитьБобрят()
        {
            echo "Учу математике\n";
        }
    }
    ```

    Хорошо (каждый занимается своим делом):

    ```php
    <?php

    class БобёрСтроитель
    {
        public function строитьПлотину()
        {
            echo "Строю крепкую плотину\n";
        }
    }

    class МедведьРыбак
    {
        public function ловитьРыбу()
        {
            echo "Ловлю рыбу в реке\n";
        }
    }

    class ЛисаПовар
    {
        public function готовитьЕду()
        {
            echo "Готовлю вкусный обед\n";
        }
    }

    class СоваУчитель
    {
        public function учитьЗверят()
        {
            echo "Учу математике\n";
        }
    }
    ```

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

??? info "Сказка о Зайкиной норке"

    Зайчиха построила норку с одной дверью. Но стоило прийти гостям, начинались проблемы: для Ёжика с иголками приходилось подтачивать вход, для Медвежонка — ломать стену и расширять проход. После каждого гостя приходилось делать ремонт.

    Мудрая Сова подсказала: «Сделай такую норку, чтобы можно было менять двери, не трогая стены. Пусть норка остаётся как есть, а двери поставим разные».

    Плохо (меняем саму норку под каждого гостя):

    ```php
    <?php

    class Норка
    {
        public function впуститьГостя($гость)
        {
            if ($гость == "ёжик") {
                echo "Перестраиваю вход для иголок\n";
            } elseif ($гость == "медвежонок") {
                echo "Расширяю дверь для медвежонка\n";
            }
        }
    }
    ```

    Хорошо (добавляем новые типы дверей без изменения норки):

    ```php
    <?php

    interface Дверь
    {
        public function открыть();
    }

    class ОбычнаяДверь implements Дверь
    {
        public function открыть()
        {
            echo "Открываю обычную дверь\n";
        }
    }

    class ШирокаяДверь implements Дверь
    {
        public function открыть()
        {
            echo "Открываю широкую дверь для больших гостей\n";
        }
    }

    class МягкаяДверь implements Дверь
    {
        public function открыть()
        {
            echo "Открываю мягкую дверь для колючих друзей\n";
        }
    }

    class Норка
    {
        public function впуститьГостя(Дверь $дверь)
        {
            $дверь->открыть();
        }
    }
    ```

* [Принцип открытости/закрытости](https://laravel.su/library/solid#princip-otkrytostizakrytosti)

## L — Liskov Substitution Principle (Принцип подстановки Лисков), LSP

> Рождённый ползать летать не может.

Подклассы должны дополнять, а не замещать поведение базового класса.

LSP — это про предсказуемость.

Проблемный дизайн:

```php
<?php

class Employee
{
    public function calculateSalary(): float
    {
        return 50000; // Базовая зарплата
    }

    public function work(): string
    {
        return "Сотрудник работает";
    }
}

class FullTimeEmployee extends Employee
{
    // Штатный сотрудник
}

class Intern extends Employee
{
    public function calculateSalary(): float
    {
        throw new Exception("Стажеры не получают зарплату, только стипендию!");
    }
}
```

Решение:

```php
<?php

interface Worker
{
    public function work(): string;
}

interface PaidWorker extends Worker
{
    public function calculateSalary(): float;
}

class FullTimeEmployee implements PaidWorker
{
    public function work(): string
    {
        return "Штатный сотрудник работает 8 часов";
    }

    public function calculateSalary(): float
    {
        return 50000;
    }
}

class Intern implements Worker
{
    public function work(): string
    {
        return "Стажер учится и помогает";
    }

    // Нет метода calculateSalary() - стажеры не получают зарплату
}

class Contractor implements PaidWorker
{
    public function work(): string
    {
        return "Фрилансер выполняет проект";
    }

    public function calculateSalary(): float
    {
        return 75000; // Почасовая оплата
    }
}

// Функции для работы с оплатой
function processPayroll(PaidWorker $worker)
{
    echo $worker->work() . "\n";
    echo "Зарплата: " . $worker->calculateSalary() . "\n";
}

function trackWork(Worker $worker)
{
    echo "Отслеживание: " . $worker->work() . "\n";
}
```

Использование:

```php
<?php

$fullTime = new FullTimeEmployee();
$intern = new Intern();
$contractor = new Contractor();

processPayroll($fullTime);   // OK
processPayroll($contractor); // OK
// processPayroll($intern);   // Ошибка - стажер не PaidWorker

trackWork($fullTime);   // OK
```

### Что ещё почитать?

??? info "Сказка о птичьей почте"

    В лесу работала птичья почта. Аист, Воробей и Ворона спокойно летали и доставляли письма. Однажды туда устроили Пингвина: формально он ведь тоже птица. Но как только ему дали письмо в соседний лес, система сломалась — Пингвин просто не мог взлететь.

    Мудрая Сова сказала: «Если кто‑то подставляется вместо другого, он должен уметь делать всё то же самое, иначе всё развалится».

    Плохо (Пингвин не может заменить летающую птицу):

    ```php
    <?php

    class ЛетающаяПтица
    {
        public function летать()
        {
            echo "Лечу по небу\n";
        }
    }

    class Пингвин extends ЛетающаяПтица
    {
        public function летать()
        {
            throw new Exception("Я не умею летать!");
        }
    }
    ```

    Хорошо (правильная иерархия):

    ```php
    <?php

    class Птица
    {
        public function издаватьЗвук()
        {
            echo "Чирик!\n";
        }
    }

    class ЛетающаяПтица extends Птица
    {
        public function летать() {
            echo "Лечу по небу\n";
        }
    }

    class НелетающаяПтица extends Птица
    {
        public function бегать() {
            echo "Быстро бегу\n";
        }
    }

    class Воробей extends ЛетающаяПтица {}

    class Пингвин extends НелетающаяПтица {}

    // Птичья почта использует только летающих птиц
    class ПтичьяПочта
    {
        public function доставитьПисьмо(ЛетающаяПтица $птица)
        {
            $птица->летать();
        }
    }
    ```

* [Принцип подстановки Барбары Лисков](https://laravel.su/library/solid#princip-podstanovki-barbary-liskov)

## I — Interface Segregation Principle (Принцип разделения интерфейсов), ISP

> Лучше меньше, да лучше.

Клиенты не должны зависеть от неиспользуемых ими методов.

Лучше применять несколько небольших интерфейсов с используемыми методами, чем один большой с кучей методов, которые необходимо реализовывать, даже если вам они не нужны.

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

??? info "Сказка о лесной спартакиаде"

    Звери решили устроить спартакиаду, собравшись на поляне с небольшим озером. Лиса-организатор объявила: «Каждый участник должен уметь бегать, плавать, летать и рыть норы». На поляне повисла пауза.

    Рыбка смутилась: «Я умею только плавать…»

    Птичка опустила крылья: «А я — только летать…»

    Крот пожал плечами: «Могу рыть норы, но до бега и полётов мне далеко».

    Сова вмешалась: «Не надо заставлять всех всё уметь. Пусть у каждого будет свой набор навыков, и отдельные соревнования для каждого типа навыка».

    Плохо (все должны уметь всё):

    ```php
    <?php

    interface УчастникСпартакиады
    {
        public function бегать();

        public function плавать();

        public function летать();

        public function рытьНору();
    }

    class Рыбка implements УчастникСпартакиады
    {
        public function бегать()
        {
            throw new Exception("Не умею!");
        }

        public function плавать()
        {
            echo "Плыву!\n";
        }

        public function летать()
        {
            throw new Exception("Не умею!");
        }

        public function рытьНору()
        {
            throw new Exception("Не умею!");
        }
    }
    ```

    Хорошо (каждый выбирает свои способности):

    ```php
    <?php

    interface Бегун
    {
        public function бегать();
    }

    interface Пловец
    {
        public function плавать();
    }

    interface Летун
    {
        public function летать();
    }

    interface Землекоп
    {
        public function рытьНору();
    }

    class Рыбка implements Пловец
    {
        public function плавать()
        {
            echo "Плыву быстро!\n";
        }
    }

    class Утка implements Пловец, Летун
    {
        public function плавать()
        {
            echo "Плыву по пруду\n";
        }

        public function летать() {
            echo "Взлетаю в небо\n";
        }
    }

    class Крот implements Землекоп
    {
        public function рытьНору()
        {
            echo "Рою глубокую нору\n";
        }
    }
    ```

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

??? info "Сказка о Медвежьей закусочной"

    Медведь открыл закусочную и нанял Зайца-повара. Заяц готовил только морковные блюда, и Медведь перенимал у него именно эти рецепты. Пока Заяц был на месте, всё шло гладко.

    Но однажды Заяц заболел, и его заменил Барсук-повар с совсем другими блюдами. Медведь растерялся: он привык к одному стилю и не умел работать по‑другому.

    Сова сказала: «Учись не у конкретного повара, а изучай общие принципы кулинарии. Тогда любой повар сможет подойти — хоть Заяц, хоть Барсук, хоть Лиса».

    Плохо (Медведь жёстко привязан к Зайцу):

    ```php
    <?php

    class ЗаяцПовар
    {
        public function готовить()
        {
            echo "Готовлю морковный салат\n";
        }
    }

    class МедведьХозяин
    {
        private $заяц;

        public function __construct()
        {
            $this->заяц = new ЗаяцПовар(); // Привязан к Зайцу!
        }

        public function обслужитьГостя()
        {
            $this->заяц->готовить();
        }
    }
    ```

    Хорошо (Медведь работает с любым поваром):

    ```php
    <?php

    interface Повар
    {
        public function готовить();
    }

    class ЗаяцПовар implements Повар
    {
        public function готовить()
        {
            echo "Готовлю морковный салат\n";
        }
    }

    class БарсукПовар implements Повар
    {
        public function готовить()
        {
            echo "Готовлю грибной суп\n";
        }
    }

    class ЛисаПовар implements Повар
    {
        public function готовить()
        {
            echo "Готовлю ягодный пирог\n";
        }
    }

    class МедведьХозяин
    {
        private $повар;

        public function __construct(Повар $повар)
        {
            $this->повар = $повар; // Может работать с любым поваром!
        }

        public function обслужитьГостя()
        {
            $this->повар->готовить();
        }
    }

    // Использование
    $медведь = new МедведьХозяин(new ЗаяцПовар());
    $медведь->обслужитьГостя();

    // Заяц заболел? Не беда!
    $медведь = new МедведьХозяин(new БарсукПовар());
    $медведь->обслужитьГостя();
    ```

* [Принцип инверсии зависимостей](https://laravel.su/library/solid#princip-inversii-zavisimostei)
