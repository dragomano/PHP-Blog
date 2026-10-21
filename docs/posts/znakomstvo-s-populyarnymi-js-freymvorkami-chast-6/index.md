---
title: 'Знакомство с популярными JS фреймворками - Solid.js'
description: 'Изучаем Solid.js на простом примере.'
og_image: solid.png
slug: znakomstvo-s-populyarnymi-js-freymvorkami-chast-6
date: 2023-10-25
tags:
  - JS
  - Solid
---

А вот вам и вариант фреймворка, который похож как на React, так и на Svelte. А своим размером он не уступает Preact. Встречайте — Solid!

<!-- more -->

![](solid.png)

## В этой серии

- [Часть 1: создание компонента на Alpine.js](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-1/index.md){ data-preview }
- [Часть 2: почему Vue?](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-2/index.md){ data-preview }
- [Часть 3: знакомство с React](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-3/index.md){ data-preview }
- [Часть 4: а может Preact?](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-4/index.md){ data-preview }
- [Часть 5: Svelte тоже неплох](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-5/index.md){ data-preview }
- Часть 6: но и Solid красавчик ⬅️ вы здесь
- [Заключение: подводим итоги](../znakomstvo-s-populyarnymi-js-freymvorkami-zaklyuchenie/index.md){ data-preview }

## Вступление

Можете взять за основу любой из предыдущих проектов, либо начать с нуля. Решать вам.

## Подготовка

Итак, перейдите в папку `projects`, откройте консоль и запустите следующую команду:

=== ":simple-npm: npm"
    ```bash
    npm create vite@latest solid-todo -- --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    npm i -D unocss @iconify-json/heroicons
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm create vite solid-todo --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    pnpm add -D unocss @iconify-json/heroicons
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn create vite solid-todo --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    yarn add -D unocss @iconify-json/heroicons
    ```

=== ":simple-bun: Bun"
    ```bash
    bun create vite solid --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    bun add -D unocss @iconify-json/heroicons
    ```

Шаблон Vite пока ставит первую версию Solid, а мы будем писать на второй. Во второй версии DOM-часть вынесена в отдельный пакет `@solidjs/web`, а компилятор JSX — в плагин `@solidjs/vite-plugin`, который заменяет собой `vite-plugin-solid`:

=== ":simple-npm: npm"
    ```bash
    npm i solid-js@2.0.0-rc.16 @solidjs/web@2.0.0-rc.16
    npm i -D @solidjs/vite-plugin@3.0.0-next.50
    npm uninstall vite-plugin-solid
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm add solid-js@2.0.0-rc.16 @solidjs/web@2.0.0-rc.16
    pnpm add -D @solidjs/vite-plugin@3.0.0-next.50
    pnpm remove vite-plugin-solid
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn add solid-js@2.0.0-rc.16 @solidjs/web@2.0.0-rc.16
    yarn add -D @solidjs/vite-plugin@3.0.0-next.50
    yarn remove vite-plugin-solid
    ```

=== ":simple-bun: Bun"
    ```bash
    bun add solid-js@2.0.0-rc.16 @solidjs/web@2.0.0-rc.16
    bun add -D @solidjs/vite-plugin@3.0.0-next.50
    bun remove vite-plugin-solid
    ```

!!! note "Примечание"

    Второй Solid ещё не вышел: на момент написания статьи актуальна версия `2.0.0-rc.16`, и до релиза её API ещё может меняться. Версии в командах выше указаны явно — если возьмёте более свежие, сверяйтесь с [руководством по миграции](https://github.com/solidjs/solid/blob/next/documentation/solid-2.0/MIGRATION.md).

и обновите `vite.config.js`:

```js
import { defineConfig } from 'vite'
import UnoCSS from 'unocss/vite'
import solid from '@solidjs/vite-plugin'

export default defineConfig({
  plugins: [UnoCSS(), solid()],
})
```

Добавьте `uno.config.js`:

```js
import { defineConfig, presetIcons, presetWind4 } from 'unocss'

export default defineConfig({
  presets: [
    presetWind4(),
    presetIcons(),
  ],
})
```

`App.css` можно удалить, он нам не нужен.

Обновите `src/index.jsx`:

```jsx
/* @refresh reload */
import { render } from '@solidjs/web'

import 'virtual:uno.css'
import App from './App'

const root = document.getElementById('root')

render(() => <App />, root)
```

Файл `src/App.jsx`:

```jsx
import TodoList from './components/TodoList';

function App() {
  return <TodoList title='Список дел' />;
}

export default App;
```

Сможете найти отличия от React?

Осталось запустить dev-сервер и начать создавать компоненты:

=== ":simple-npm: npm"
    ```bash
    npm run dev
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm run dev
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn dev
    ```

=== ":simple-bun: Bun"
    ```bash
    bun run dev
    ```

## Компонент `TodoList`

Как и прежде, сначала создадим компонент списка. Создайте в директории `src/components` файл `TodoList.jsx`:

```jsx
import { createStore } from "solid-js";

function TodoList(props) {
  const [todos, setTodos] = createStore([]);

  return (
    <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      <ul class='list-none p-4'></ul>
    </div>
  );
}

export default TodoList;
```

Здесь мы с помощью `createStore` создаём реактивное хранилище — близкий родственник `useState` в React или `useSignal` в Preact, но рассчитанный на объекты и массивы. Читается оно как обычный объект (`todos.length`), а меняется через вторую половину пары — сеттер `setTodos`.

Получать список текущих задач мы, как и раньше, будем с сервера `https://dummyjson.com/todos`. В Solid асинхронность — это обычное вычисление, поэтому источник данных описывается прямо при создании хранилища:

```jsx
import { Loading, createStore } from "solid-js";

function TodoList(props) {
  const [todos, setTodos] = createStore(
    async () => {
      const response = await fetch('https://dummyjson.com/todos');
      const data = await response.json();
      return data.todos.slice(0, 10);
    },
    []
  );

  return (
    <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      <Loading fallback={<p class='p-4 text-center text-gray-400'>Загрузка…</p>}>
        <ul class='list-none p-4'></ul>
      </Loading>
    </div>
  );
}
```

`createStore` здесь получает функцию и начальное значение — это производная форма: хранилище само вызовет функцию и разложит пришедший массив по ключу `id`, сохранив идентичность элементов. Пока ответ не пришёл, чтение из хранилища считается «не готовым», и граница `<Loading>` показывает запасной вариант — она заменяет собой `<Suspense>` и `createResource` из первой версии. Хук `onMount`, которым загрузка делалась раньше, во второй версии тоже заменён (на `onSettled`), но здесь он уже не нужен: загрузка описана там же, где живут данные.

Далее, создадим заготовки компонентов `TodoItem.jsx` и `TodoForm.jsx` и используем их в разметке:

```jsx
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';
import { For, Loading, createStore } from "solid-js";

function TodoList(props) {
  const [todos, setTodos] = createStore(
    async () => {
      const response = await fetch('https://dummyjson.com/todos');
      const data = await response.json();
      return data.todos.slice(0, 10);
    },
    []
  );

  // Заготовки для методов действий, которые определим позже
  const addTask = (title) => {};

  const toggleTask = (id) => {};

  const deleteTask = (id) => {};

  return (
    <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      <Loading fallback={<p class='p-4 text-center text-gray-400'>Загрузка…</p>}>
        <ul class='list-none p-4'>
          <For each={todos}>
            {t => <TodoItem task={t} onToggle={toggleTask} onRemove={deleteTask} />}
          </For>
        </ul>
      </Loading>
      <TodoForm onSubmit={addTask} />
    </div>
  );
}

export default TodoList;
```

Обратите внимание на использование встроенного компонента `For` в качестве управляющей конструкции для вывода всех задач в цикле.

Осталось реализовать методы управления задачами (добавление, переключение статуса и удаление), которые мы будем передавать в компоненты `TodoItem` и `TodoForm`, соответственно:

```jsx
const addTask = (title) => {
  if (!title) return;

  setTodos(t => { t.push({ id: crypto.randomUUID(), todo: title, completed: false }) });
}

const toggleTask = (id) => {
  setTodos(t => {
    const todo = t.find(todo => todo.id === id);
    if (todo) todo.completed = !todo.completed;
  });
};

const deleteTask = (id) => {
  setTodos(t => {
    const index = t.findIndex(todo => todo.id === id);
    if (index !== -1) t.splice(index, 1);
  })
}
```

Здесь важно не переносить привычки из первой версии. Сеттер во второй версии принимает функцию-черновик, и данные нужно менять прямо в ней: `push`, присваивание поля, `splice`. Если вместо этого собрать новый массив (`filter`, спред) и вернуть его, хранилище предупредит: `IMMUTABLE_UPDATE_IN_STORE`. Оно отслеживает отдельные значения, поэтому новый контейнер заставит перезапуститься всех, кто читает этот путь, хотя изменился всего один элемент. По той же причине ушли старые формы записи — путь в аргументах (`setStore('todos', ...)`) и поиск элемента предикатом: теперь нужный элемент находится внутри черновика через `find` или `findIndex`.

Напоследок добавим условие отображения списка только при ненулевом количестве задач:

```jsx
return (
  <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
    <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
    <Loading fallback={<p class='p-4 text-center text-gray-400'>Загрузка…</p>}>
      <Show when={todos.length > 0}>
        <ul class='list-none p-4'>
          <For each={todos}>
            {t => <TodoItem task={t} onToggle={toggleTask} onRemove={deleteTask} />}
          </For>
        </ul>
      </Show>
    </Loading>
    <TodoForm onSubmit={addTask} />
  </div>
);
```

Не забудьте импортировать `Show` из `solid-js`. Отдельный мемо для длины списка, которым это делалось в первой версии, больше не нужен: хранилище отслеживает чтение по свойствам, поэтому `todos.length` прямо в разметке пересчитается само.

## Компонент `TodoItem`

Обратите внимание на разметку. Solid, хоть и похож на React, но не требует писать `className` вместо `class` — и обходится без внешних библиотек вроде `clx`: условные классы записываются объектом прямо в атрибут `class`.

```jsx
function TodoItem(props) {
  const toggleTask = () => props.onToggle(props.task.id);
  const deleteTask = () => props.onRemove(props.task.id);

  return (
    <li class='flex items-center mb-2 hover:cursor-pointer' onClick={toggleTask}>
      <input type='checkbox' class='mr-2' checked={props.task.completed} readOnly />
      <span class={{ 'line-through': props.task.completed }}>{props.task.todo}</span>
      <div class="ml-auto text-gray-400 hover:text-gray-600">
        <button class="i-heroicons-trash w-6 h-6" onClick={deleteTask} />
      </div>
    </li>
  );
}

export default TodoItem;
```

Пропсы здесь читаются через `props`, а не разбираются в аргументах функции. Это тоже требование второй версии, а не вкусовщина: запись вида `function TodoItem({ task })` разворачивает значение один раз, и дальше компонент перестаёт реагировать на изменения — в dev-режиме Solid об этом предупредит. Специального атрибута `classList` из первой версии тоже больше нет, его роль целиком перешла к `class`.

!!! note "Примечание"

    События в Solid записываются в camelCase — `onClick`, `onPointerDown`. Строчное `onclick` обработчиком во второй версии не считается: это обычный HTML-атрибут, и функция в него попадёт строкой. В dev-режиме о такой опечатке предупредят (код `LOWERCASE_EVENT_ATTRIBUTE`).

## Компонент `TodoForm`

А здесь мы просто определяем переменную `inputRef` и связываем её с помощью атрибута `ref` с элементом `input`:

```jsx
function TodoForm(props) {
  let inputRef;

  const addTask = () => {
    // Передаем значение текстового ввода
    props.onSubmit(inputRef.value);

    // Очищаем текстовый ввод
    inputRef.value = '';

    // И фокусируемся на нём
    inputRef.focus();
  };

  return (
    <div class='p-4 bg-gray-100'>
      <div class='flex items-center'>
        <input
          ref={el => (inputRef = el)}
          type='text'
          class='flex-1 mr-2 py-2 px-4 rounded-md border border-gray-300'
          placeholder='Новая задача'
          autofocus
        />
        <button
          class='bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md'
          onClick={addTask}
        >
          Добавить
        </button>
      </div>
    </div>
  );
}

export default TodoForm;
```

В документации второй версии `ref` — это функция, которая получает элемент, поэтому присваивание пишем явно. Встроенные атрибуты тоже приведены к HTML и записываются строчными буквами, как здесь — `autofocus` вместо `autoFocus`.

## Документация

Если вы заинтересовались Solid JS, загляните на [официальный сайт](https://www.solidjs.com) или в [переведённую документацию](https://soliddev.ru/guides/).

У второй версии документация отдельная — [v2.solidjs.com](https://v2.solidjs.com), — и там же пригодится [руководство по миграции](https://github.com/solidjs/solid/blob/next/documentation/solid-2.0/MIGRATION.md), если у вас уже есть проект на первой версии.

Сравнить Solid с другими фреймворками можно [здесь](https://www.solidjs.com/guides/comparison).

## Заключение

Итак, мы закончили наше простое приложение **TODO** на Solid JS:

- успешно адаптировали исходную разметку для использования с Solid
- познакомились с управляющими конструкциями библиотеки (`For`, `Show`) и границей `<Loading>` для асинхронных данных
- нашли много похожих элементов (включая названия хуков и методов) из других фреймворков/библиотек

В [следующей части](../znakomstvo-s-populyarnymi-js-freymvorkami-zaklyuchenie/index.md) этой серии мы наконец подведём итоги.

---

[Скачать готовый проект](https://gitlab.com/dragomano/solid-todo){ .md-button .md-button--primary }
