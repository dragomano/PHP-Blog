---
title: 'Знакомство с популярными JS фреймворками - React.js'
description: 'Изучаем React.js на простом примере.'
og_image: reactjs.png
slug: znakomstvo-s-populyarnymi-js-freymvorkami-chast-3
date: 2023-07-22
tags:
  - JS
  - React
---

Добро пожаловать в обзорную статью о библиотеке React. Посмотрим, как она поможет справиться с нашим проектом.

<!-- more -->

![](reactjs.png)

## В этой серии

- [Часть 1: создание компонента на Alpine.js](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-1/index.md){ data-preview }
- [Часть 2: почему Vue?](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-2/index.md){ data-preview }
- Часть 3: знакомство с React ⬅️ вы здесь
- [Часть 4: а может Preact?](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-4/index.md){ data-preview }
- [Часть 5: Svelte тоже неплох](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-5/index.md){ data-preview }
- [Часть 6: но и Solid красавчик](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-6/index.md){ data-preview }
- [Заключение: подводим итоги](../znakomstvo-s-populyarnymi-js-freymvorkami-zaklyuchenie/index.md){ data-preview }

## Вступление

В данном случае перед нами не фреймворк, а удобная JS-библиотека для создания реактивных приложений. Но не огорчайтесь, это не недостаток, а скорее достоинство.

Оформлять код мы будем в файлах с расширением JSX — это такое специальное расширение языка JavaScript, позволяющее писать HTML и JavaScript код вместе, без использования тега `<script>`.

!!! note "Примечание"

    Из особенностей перехода с обычной разметки на JSX: в [исходной вёрстке проекта](https://drive.proton.me/urls/ZS9YYVXK38#mY7BnjYmTPGg) (если вы захотите реализовать всё с нуля) нужно заменить `class` на `className`, а все атрибуты в `kebab-case` — на `camelCase`.

## Подготовка

Итак, перейдите в папку `projects`, откройте консоль и запустите следующую команду:

=== ":simple-npm: npm"
    ```bash
    npm create vite@latest react-todo -- --template react
    ```

    Теперь перейдите в созданную папку `react-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    npm i -D unocss @iconify-json/heroicons
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm create vite react-todo --template react
    ```

    Теперь перейдите в созданную папку `react-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    pnpm add -D unocss @iconify-json/heroicons
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn create vite react-todo --template react
    ```

    Теперь перейдите в созданную папку `react-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    yarn add -D unocss @iconify-json/heroicons
    ```

=== ":simple-bun: Bun"
    ```bash
    bun create vite react --template react
    ```

    Теперь перейдите в созданную папку `react-todo` и установите [UnoCSS](https://dragomano.github.io/unocss-russian/):

    ```bash
    bun add -D unocss @iconify-json/heroicons
    ```

и обновите `vite.config.js`:

```js
import { defineConfig } from 'vite'
import UnoCSS from 'unocss/vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [UnoCSS(), react()],
});
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

Обновите `src/main.jsx`:

```jsx
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import 'virtual:uno.css'

createRoot(document.getElementById('root')).render(
  <App />
)
```

Как и ранее, мы создадим 3 компонента, не считая корневого (`App.jsx`). Но прежде добавьте класс `bg-gray-200` элементу `body` в файле `index.html`, чтобы у страницы был серый фон.

Запускаем проект:

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

## App.jsx

Перепишите код файла `src/App.jsx`:

```jsx
import TodoList from './components/TodoList';

function App() {
  return <TodoList title='Список дел' />;
}

export default App;
```

Как видите, компоненты в React представляют собой обычные функции (и потому называются _функциональными_) с параметрами (_props_). Чтобы компонент был доступен извне (для использования в скриптах или в других компонентах), функцию нужно экспортировать:

```js
export default App;
```

Каждая такая функция возвращает строку в JSX формате, без всяких экранирований и кавычек. Например: `<div></div>`. Когда возвращаемый блок большой, его требуется окружить круглыми скобками:

```jsx
return (
  <div>
    <h1>Заголовок</h1>
  </div>
);
```

## TodoList.jsx

Итак, после переделки нашей вёрстки (см. [Вступление](#vstuplenie)) мы можем использовать её в первом компоненте:

```jsx
function TodoList(props) {
  return (
    <div className="max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden">
      <h1 className="text-2xl font-bold text-center py-4 bg-gray-100">Список дел</h1>
      <ul className="list-none p-4">
        <li className="flex items-center mb-2 hover:cursor-pointer">
          <input type="checkbox" className="mr-2" checked>
          <span className="line-through">Вымыть пол</span>
          <div class="ml-auto text-gray-400 hover:text-gray-600">
            <button class="i-heroicons-trash w-6 h-6" />
          </div>
        </li>
      </ul>
      <div className="p-4 bg-gray-100">
        <div className="flex items-center">
          <input type="text" className="flex-1 mr-2 py-2 px-4 rounded-md border border-gray-300" placeholder="Новая задача" autoFocus>
          <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md">
            Добавить
          </button>
        </div>
      </div>
    </div>
  );
}

export default TodoList;
```

Далее вынесем элемент списка и форму добавления новой задачи в отдельные компоненты, а также добавим логику React:

```jsx
import { useState, useEffect } from 'react';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';

function TodoList(props) {
  // Создаем переменные для хранения списка задач и функции для для обновления текущего списка задач
  const [todos, setTodos] = useState([]);

  // Запрашиваем список задач при обновлении страницы
  useEffect(() => {
    fetch('https://dummyjson.com/todos')
      .then((response) => response.json())
      .then((data) => {
        setTodos(data.todos.slice(0, 10));
      });
  }, []);

  // Обработчик события добавления новой задачи
  const addTask = (title) => {
    if (!title) return;

    // Обязательно используем функцию setTodos, вместо изменения массива напрямую
    setTodos((prevTodos) => [
      ...prevTodos,
      {
        id: crypto.randomUUID(),
        todo: title,
        completed: false,
      },
    ]);
  };

  // Обработчик события переключения статуса задачи
  const toggleTask = (id) => {
    setTodos((prevTodos) => prevTodos.map((t) =>
      t.id === id ? { ...t, completed: !t.completed } : t
    ));
  };

  // Обработчик события удаления задачи
  const deleteTask = (id) => {
    setTodos((prevTodos) => prevTodos.filter((todo) => todo.id !== id));
  };

  return (
    <div className='max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden'>
      <h1 className='text-2xl font-bold text-center py-4 bg-gray-100'>{props.title}</h1>
      {todos.length > 0 && (
        <ul className='list-none p-4'>
          {todos.map(t => <TodoItem key={t.id} task={t} onToggle={toggleTask} onRemove={deleteTask} />)}
        </ul>
      )}
      <TodoForm onSubmit={addTask} />
    </div>
  );
}

export default TodoList;
```

### `useReducer`

В качестве альтернативы рассмотрим ещё использование хука `useReducer` вместо `useState`:

```jsx
import { useReducer, useEffect } from 'react';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';

const taskReducer = (todos, action) => {
  switch (action.type) {
    case 'add':
      return [
        ...todos,
        {
          id: crypto.randomUUID(),
          todo: action.title,
          completed: false,
        },
      ];

    case 'toggle':
      return todos.map((t) =>
        t.id === action.id ? { ...t, completed: !t.completed } : t
      );

    case 'delete':
      return todos.filter((t) => t.id !== action.id);

    case 'set':
      return action.todos;

    default:
      throw new Error('Неизвестное действие: ' + action.type);
  }
}

function TodoList(props) {
  const [todos, dispatch] = useReducer(taskReducer, []);

  useEffect(() => {
    fetch('https://dummyjson.com/todos')
      .then((response) => response.json())
      .then((data) => {
        dispatch({ type: 'set', todos: data.todos.slice(0, 10) });
      });
  }, []);

  const addTask = (title) => {
    if (!title) return;
    dispatch({ type: 'add', title });
  };

  const toggleTask = (id) => {
    dispatch({ type: 'toggle', id });
  };

  const deleteTask = (id) => {
    dispatch({ type: 'delete', id });
  };

  return (
    // вывод такой же, как и выше
  );
}

export default TodoItem;
```

Какой из вариантов вам больше нравится, тот и используйте.


## TodoItem.jsx

```jsx
function TodoItem({ task, onToggle, onRemove }) {
  // Обработчик события изменения статуса задачи
  const toggleTask = () => onToggle(task.id);

  // Обработчик события удаления задачи
  const deleteTask = (e) => {
    // Добавляем, чтобы обрабатывался именно клик на кнопке удаления, а не на всем элементе списка
    e.stopPropagation();

    // Отправляем id удаляемого элемента в метод родительского компонента
    onRemove(task.id);
  };

  return (
    <li className='flex items-center mb-2 hover:cursor-pointer' onClick={toggleTask}>
      <input type='checkbox' className='mr-2' checked={task.completed} readOnly />
      <span className={todo.completed ? 'line-through' : ''}>{task.title}</span>
      <div class="ml-auto text-gray-400 hover:text-gray-600">
        <button class="i-heroicons-trash w-6 h-6" onClick={deleteTask} />
      </div>
    </li>
  );
}

export default TodoItem;
```

!!! note "Примечание"

    Запомните, `useState` позволяет настроить СОСТОЯНИЕ заданной переменной, а не её СТОЯНИЕ, как иногда можно услышать на собеседованиях. Например, следующий код объявляет переменную `counter` с начальным значением `1`, а также функцию `setCounter`, предназначенную для изменения этой переменной. То есть в React нельзя обновлять состояние простым перезаписыванием переменной, если вы хотите, чтобы она была по-настоящему реактивной:

    ```
    import { useState } from 'react'

    const [counter, setCounter] = useState(1)
    ```

Обратите внимание, что мы разложили входные параметры (`props`), для удобства использования в коде (`task.title` вместо `props.task.title` и т. д.).

## TodoForm.jsx

```jsx
import { useRef } from 'react';

function TodoForm(props) {
  // Создаем переменную-ссылку для связывания с элементом <input> через атрибут ref
  const inputRef = useRef(null);

  // Обработчик события добавления новой задачи
  const addTask = () => {
    // Передаем введённый в поле текст далее, родительскому компоненту
    props.onSubmit(inputRef.current.value);

    inputRef.current.value = '';
    inputRef.current.focus();
  };

  return (
    <div className='p-4 bg-gray-100'>
      <div className='flex items-center'>
        <input
          ref={inputRef}
          type='text'
          className='flex-1 mr-2 py-2 px-4 rounded-md border border-gray-300'
          placeholder='Новая задача'
          autoFocus
        />
        <button
          className='bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md'
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

Обратите внимание, что в React нет нужды в чём-то типа `r-model` и прочего, всё удобно реализуется через один атрибут `ref` и хук `useRef`.

## Документация

Если вы заинтересовались React, загляните в [локализованный справочник](https://reactdev.ru). Новичкам также пригодится короткий [вступительный ролик](https://www.youtube.com/watch?v=GeulXZP_kZ8).

## Заключение

Итак, мы закончили наше простое приложение **TODO** на React.js:

- успешно изменили исходную вёрстку в соответствии с требованиями библиотеки
- познакомились с основными директивами React и форматом JSX
- настроили валидацию входных параметров в компонентах

В [следующей части](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-4/index.md) этой серии мы познакомимся с Preact.

---

[Скачать готовый проект](https://gitlab.com/dragomano/react-todo){ .md-button .md-button--primary }
