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

    Теперь перейдите в созданную папку `solid-todo` и установите `tailwindcss`:

    ```bash
    npm i -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm create vite solid-todo --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите `tailwindcss`:

    ```bash
    pnpm add -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn create vite solid-todo --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите `tailwindcss`:

    ```bash
    yarn add -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-bun: Bun"
    ```bash
    bun create vite solid --template solid
    ```

    Теперь перейдите в созданную папку `solid-todo` и установите `tailwindcss`:

    ```bash
    bun add -D tailwindcss@next @tailwindcss/vite@next
    ```

и обновите `vite.config.js`:

```js
import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [solid(), tailwindcss()],
})
```

В файл `src/index.css` замените всё содержимое на следующий код:

```css
@import "tailwindcss";
```

`App.css` можно удалить, он нам не нужен.

Файл `src/index.jsx` оставляем без изменений.

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
import { createStore } from "solid-js/store";

function TodoList(props) {
  const [store, setStore] = createStore({ todos: [] });

  return (
    <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      <ul class='list-none p-4'></ul>
    </div>
  );
}

export default TodoList;
```

Здесь мы с помощью `createSignal` (аналог `useState` в React, или `useSignal` в Preact) определяем две функции — `todos` и `setTodos`. Первая будет возвращать список задач, а вторая — обновлять этот список.

Получать список текущих задач мы, как и раньше, будем с сервера `https://dummyapi.online/api/todos`, с использованием хука жизненного цикла `onMount` — не забудьте импортировать его из `solid-js`:

```jsx
import { onMount } from "solid-js";
import { createStore } from "solid-js/store";

function TodoList(props) {
  const [store, setStore] = createStore({ todos: [] });

  onMount(() => {
    fetch('https://dummyapi.online/api/todos')
      .then(response => response.json())
      .then(data => setStore('todos', data.slice(0, 10)))
  })

  // ...
}
```

Далее, создадим заготовки компонентов `TodoItem.jsx` и `TodoForm.jsx` и используем их в разметке:

```jsx
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';
import { onMount, For } from "solid-js";
import { createStore } from "solid-js/store";

function TodoList(props) {
  const [store, setStore] = createStore({ todos: [] });

  onMount(() => {
    fetch('https://dummyapi.online/api/todos')
      .then(response => response.json())
      .then(data => setStore('todos', data.slice(0, 10)))
  })

  // Заготовки для методов действий, которые определим позже
  const addTodo = (title) => {};

  const toggleTodo = (id) => {};

  const deleteTodo = (id) => {};

  return (
    <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      <ul class='list-none p-4'>
        <For each={store.todos}>
          {(todo) => (
            <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} onRemove={deleteTodo} />
          )}
        </For>
      </ul>
      <TodoForm onSubmit={addTodo} />
    </div>
  );
}

export default TodoList;
```

Обратите внимание на использование встроенного компонента `For` в качестве управляющей конструкции для вывода всех задач в цикле.

Осталось реализовать методы управления задачами (добавление, переключение статуса и удаление), которые мы будем передавать в компоненты `TodoItem` и `TodoForm`, соответственно:

```jsx
const addTodo = (title) => {
  if (!title) return;

  setStore('todos', (todos) => [...todos, { id: crypto.randomUUID(), title, completed: false }]);
}

const toggleTodo = (id) => {
  setStore('todos', (t) => t.id === id, 'completed', (completed) => !completed);
};

const deleteTodo = (id) => {
  setStore('todos', (t) => t.filter((t) => t.id !== id))
}
```

Заметили, как осуществляется доступ к массиву задач, хранящемуся в `todos`? Через вызов функции `todos()`.

Напоследок добавим условие отображения списка только при ненулевом количестве задач:

```jsx
// Используем сигнал, доступный только для чтения
const length = createMemo(() => store.todos.length);

return (
  <div class='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
    <h1 class='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
    {length() > 0 && (
      <ul class='list-none p-4'>
        <For each={store.todos}>
          {(todo) => (
            <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} onRemove={deleteTodo} />
          )}
        </For>
      </ul>
    )}
    <TodoForm onSubmit={addTodo} />
  </div>
);
```

Не забудьте импортировать `createMemo` (аналог `computed` во Vue) из `solid-js`.

## Компонент `TodoItem`

Обратите внимание на разметку. Solid, хоть и похож на React, но не требует написания `className` вместо `class`, а также имеет некоторые специальные атрибуты JSX (например, `classList`, позволяющий обойтись без внешних библиотек типа `clx`).

```jsx
function TodoItem({ todo, onToggle, onRemove }) {
  const toggleTodo = () => onToggle(todo.id);
  const deleteTodo = () => onRemove(todo.id);

  return (
    <li class='flex items-center mb-2 hover:cursor-pointer' onClick={toggleTodo}>
      <input type='checkbox' class='mr-2' checked={todo.completed} readOnly />
      <span classList={{ 'line-through': todo.completed }}>{todo.title}</span>
      <div class='ml-auto'>
        <button class='text-gray-400 hover:text-gray-600' onClick={deleteTodo}>
          <svg
            xmlns='http://www.w3.org/2000/svg'
            fill='none'
            viewBox='0 0 24 24'
            strokeWidth='1.5'
            stroke='currentColor'
            class='w-6 h-6'
          >
            <path
              strokeLinecap='round'
              strokeLinejoin='round'
              d='M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0'
            />
          </svg>
        </button>
      </div>
    </li>
  );
}

export default TodoItem;
```

!!! note "Примечание"

    Обработчики событий в Solid обычно имеют форму `onclick` или `onClick` в зависимости от стиля. А вот название самого события всегда в нижнем регистре.

## Компонент `TodoForm`

А здесь мы просто определяем переменную `inputRef` и связываем её с помощью атрибута `ref` с элементом `input`:

```jsx
function TodoForm(props) {
  let inputRef;

  const addTodo = () => {
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
          ref={inputRef}
          type='text'
          class='flex-1 mr-2 py-2 px-4 rounded-md border border-gray-300'
          placeholder='Новая задача'
          autoFocus
        />
        <button
          class='bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md'
          onClick={addTodo}
        >
          Добавить
        </button>
      </div>
    </div>
  );
}

export default TodoForm;
```

## Документация

Если вы заинтересовались Solid JS, загляните на [официальный сайт](https://www.solidjs.com) или в [переведённую документацию](https://soliddev.ru/guides/).

Сравнить Solid с другими фреймворками можно [здесь](https://www.solidjs.com/guides/comparison).

## Заключение

Итак, мы закончили наше простое приложение **TODO** на Solid JS:

- успешно адаптировали исходную разметку для использования с Solid
- познакомились с некоторыми директивами библиотеки
- нашли много похожих элементов (включая названия хуков и методов) из других фреймворков/библиотек

В [следующей части](../znakomstvo-s-populyarnymi-js-freymvorkami-zaklyuchenie/index.md) этой серии мы наконец подведём итоги.

---

[Скачать готовый проект](https://gitlab.com/dragomano/solid-todo){ .md-button .md-button--primary }
