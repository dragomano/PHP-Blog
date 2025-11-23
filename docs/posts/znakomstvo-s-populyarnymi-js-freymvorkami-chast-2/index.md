---
title: 'Знакомство с популярными JS фреймворками - Vue.js'
description: 'Изучаем Vue.js на простом примере.'
og_image: vue.png
slug: znakomstvo-s-populyarnymi-js-freymvorkami-chast-2
date: 2023-06-22
tags:
  - JS
  - Vue
---

Продолжаем обозревать известные фреймворки. И сегодня настала очередь Vue.js!

<!-- more -->

![](vue.png)

## В этой серии

- [Часть 1: создание компонента на Alpine.js](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-1/index.md){ data-preview }
- Часть 2: почему Vue? ⬅️ вы здесь
- [Часть 3: знакомство с React](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-3/index.md){ data-preview }
- [Часть 4: а может Preact?](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-4/index.md){ data-preview }
- [Часть 5: Svelte тоже неплох](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-5/index.md){ data-preview }
- [Часть 6: но и Solid красавчик](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-6/index.md){ data-preview }
- [Заключение: подводим итоги](../znakomstvo-s-populyarnymi-js-freymvorkami-zaklyuchenie/index.md){ data-preview }

## Вступление

Хорошая новость для тех, кто уже знаком с Alpine.js — синтаксис основных директив тут совпадает (потому что позаимствован разработчиком Alpine.js как раз таки у Vue.js и Angular). В большинстве случаев достаточно в вашем старом коде заменить `x-` на `v-` и считай полдела вы уже сделаете. Поэтому можно просто скопировать разметку из [предыдущего проекта](https://gitlab.com/dragomano/alpine-todo), с дальнейшей заменой директив, хотя всё-таки рекомендую работать с первоначальной [вёрсткой](https://drive.proton.me/urls/ZS9YYVXK38#mY7BnjYmTPGg).

С осени 2021 года синтаксис `<script setup>` стал рекомендуемым способом создания проектов на Vue 3. Поэтому мы изначально будем использовать новый синтаксис.

## Vue.js

Итак, перейдите в папку `projects`, откройте консоль и запустите следующую команду:

=== ":simple-npm: npm"
    ```bash
    npm create vite@latest vue-todo -- --template vue
    ```

    Теперь перейдите в созданную папку `vue-todo` и установите `tailwindcss`:

    ```bash
    npm i -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-pnpm: pnpm"
    ```bash
    pnpm create vite vue-todo --template vue
    ```

    Теперь перейдите в созданную папку `vue-todo` и установите `tailwindcss`:

    ```bash
    pnpm add -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-yarn: Yarn"
    ```bash
    yarn create vite vue-todo --template vue
    ```

    Теперь перейдите в созданную папку `vue-todo` и установите `tailwindcss`:

    ```bash
    yarn add -D tailwindcss@next @tailwindcss/vite@next
    ```

=== ":simple-bun: Bun"
    ```bash
    bun create vite vue --template vue
    ```

    Теперь перейдите в созданную папку `vue-todo` и установите `tailwindcss`:

    ```bash
    bun add -D tailwindcss@next @tailwindcss/vite@next
    ```

и обновите `vite.config.js`:

```js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), tailwindcss()],
});
```

В файл `src/style.css` замените всё содержимое на следующий код:

```css
@import "tailwindcss";
```

## Подготовка основных файлов

Обновите файл `index.html` в корне проекта:

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Список дел</title>
  </head>
  <body class="bg-gray-200">
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

Откройте файл `src/App.vue` и замените его содержимое таким образом:

```html
<script setup>
  import TodoList from './components/TodoList.vue';
</script>

<template>
  <TodoList title="Список дел" />
</template>
```

При использовании `<script setup>` импортированные компоненты автоматически становятся доступными для шаблона.

Файл `src/components/HelloWorld.vue` можно удалить, он нам не понадобится.

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

## Компонент TodoList

Создадим файл `src/components/TodoList.vue`:

```html
<script setup>
  import { ref } from 'vue';

  // Объявляем входные параметры
  defineProps({
    title: String,
  });

  // Создаем переменную-ссылку для хранения списка задач
  const todos = ref([]);
</script>

<template>
  <div class="max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden">
    <h1 class="text-2xl font-bold text-center py-4 bg-gray-100">{{ title }}</h1>
    <ul class="list-none p-4" v-show="todos.length"></ul>
  </div>
</template>
```

Обратите внимание на директиву `v-show` в разметке. С её помощью мы будем отображать список `ul` только если массив `todos` не пуст. В противном случае элемент будет скрываться с помощью CSS `display: none`.

!!! note "Примечание"

    При именовании своих компонентов всегда используйте имена из нескольких слов. Это связано с [рекомендациями Vue.js](https://v3.ru.vuejs.org/ru/style-guide/#%D0%B8%D0%BC%D0%B5%D0%BD%D0%B0-%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-%D0%B8%D0%B7-%D0%BD%D0%B5%D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%BA%D0%B8%D1%85-%D1%81%D0%BB%D0%BE%D0%B2-%D0%B2%D0%B0%D0%B6%D0%BD%D0%BE)

Как и прежде, нам понадобится загружать список дел в формате JSON при обновлении страницы. Воспользуемся готовым кодом из предыдущего проекта и адаптируем его для Vue:

```html
<script setup>
  import { ref, onMounted } from 'vue';

  // ...

  const fetchTodos = async () => {
    await fetch('https://dummyapi.online/api/todos')
      .then((response) => response.json())
      .then((data) => {
        // У переменных ссылок все значения должны записываться в свойство value
        todos.value = data.slice(0, 10);
      });
  };

  // Выполняем функцию fetchTodos во время монтировани компонента
  onMounted(fetchTodos);

  // ...
</script>
```

Как видите, во Vue хук `onMounted` это аналог директивы `x-init` (в Alpine.js). Теперь при обновлении страницы будет загружаться список дел с JSON-сервера.

Далее реализуем метод для добавления новой задачи:

```js
const addTodo = (title) => {
  if (!title) return;

  todos.value = [
    ...todos.value,
    {
      id: crypto.randomUUID(),
      title: title,
      completed: false,
    },
  ];
};
```

Добавим и методы для переключения статуса и удаления задачи:

```js
const toggleTodo = (id) => {
  todos.value = todos.value.map((t) =>
    t.id === id ? { ...t, completed: !t.completed } : t,
  );
};

const deleteTodo = (id) => {
  todos.value = todos.value.filter((todo) => todo.id !== id);
};
```

Разделение на компоненты позволит нам масштабировать приложение и упростить дальнейшую разработку. Поэтому отображение отдельной задачи и форму для добавления новой задачи мы оформим в виде отдельных компонентов.

## Компонент TodoForm

Итак, создадим файл `src/components/TodoForm.vue`:

```html
<script setup>
  import { ref } from 'vue';

  const emit = defineEmits(['submit']);

  // Создаем переменную-ссылку на элемент input с атрибутом v-model="input"
  // Теперь получить доступ к его значению можно через input.value
  const input = ref('');

  // Создаем переменную-ссылку на DOM-элемент input с атрибутом ref="newTodo" в разметке
  const newTodo = ref(null);

  // Вообще-то можно было бы не создавать переменную input и работать со значением текстового элемента через newTodo.value.value, но выглядит не очень красиво

  const addTodo = () => {
    // Отправляем из дочернего компонента (то есть отсюда) в родительский введённое значение из элемента `input`, связывая его с событием `submit`
    emit('submit', input.value);

    // Очищаем форму ввода
    input.value = '';

    // И фокусируемся на ней (мало ли, вдруг ещё одну задачу захотим сразу ввести)
    newTodo.value.focus();
  };
</script>

<template>
  <div class="p-4 bg-gray-100">
    <div class="flex items-center">
      <input
        ref="newTodo"
        v-model="input"
        type="text"
        class="flex-1 mr-2 py-2 px-4 rounded-md border border-gray-300"
        placeholder="Новая задача"
        autofocus
      />
      <button
        class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md"
        @click="addTodo"
      >
        Добавить
      </button>
    </div>
  </div>
</template>
```

Теперь компонент **TodoList** можно обновить таким образом:

```html
<script setup>
  import { ref, onMounted } from 'vue';
  import TodoForm from './TodoForm.vue';

  // ...
</script>

<template>
  <div class="max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden">
    <h1 class="text-2xl font-bold text-center py-4 bg-gray-100">{{ title }}</h1>
    <ul class="list-none p-4" v-show="todos.length"></ul>
    <TodoForm @submit="addTodo" />
  </div>
</template>
```

## Компонент TodoItem

Однако наше приложение до сих пор не выполняет первоначальную задачу — отображение списка дел. Исправим эту оплошность.

Создадим файл `src/components/TodoItem.vue`:

```html
<script setup>
  // Определяем входные параметры
  const props = defineProps({ todo: Object });

  // Определяем события, которые будем отправлять в родительский компонент
  const emit = defineEmits(['toggle', 'remove']);

  const toggleTodo = () => emit('toggle', props.todo.id);

  const deleteTodo = () => emit('remove', props.todo.id);
</script>

<template>
  <li class="flex items-center mb-2 hover:cursor-pointer" @click="toggleTodo">
    <input type="checkbox" class="mr-2" :checked="todo.completed" />
    <span :class="{ 'line-through': todo.completed }" v-text="todo.title"></span>
    <div class="ml-auto">
      <button class="text-gray-400 hover:text-gray-600" @click="deleteTodo">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
          />
        </svg>
      </button>
    </div>
  </li>
</template>
```

!!! note "Примечание"

    Во Vue разметка `<span v-text="variable"></span>` аналогична `<span>{{ variable }}</span>`. Результат отображения будет одним и тем же.

Теперь можно вызывать компонент **TodoItem** в качестве элемента списка внутри тега `ul`, не забыв прикрепить к нему соответствующие атрибуты:

```html
<script setup>
  import { ref, onMounted } from 'vue';
  import TodoItem from './TodoItem.vue';
  import TodoForm from './TodoForm.vue';

  // ...
</script>

<template>
  <div class="max-w-sm md:max-w-lg mx-auto my-10 bg-white rounded-md shadow-md overflow-hidden">
    <h1 class="text-2xl font-bold text-center py-4 bg-gray-100">{{ title }}</h1>
    <ul class="list-none p-4" v-show="todos.length">
      <TodoItem
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @toggle="toggleTodo"
        @remove="deleteTodo"
      />
    </ul>
    <TodoForm @submit="addTodo" />
  </div>
</template>
```

Гораздо больше кода, по сравнению с одним файлом в Alpine.js, не правда ли? Но зато разложено всё по кусочкам и каждый компонент можно заменить альтернативным или использовать отдельно. Например, можно создать `AnotherTodoForm` с теми же входными параметрами и методами, что и в `TodoForm`, но с другой HTML-разметкой, и задействовать его в `TodoList` вместо `TodoForm`.

Ниже на странице можно найти ссылки на готовый проект сразу в двух версиях — на устаревшем Options API и на современном Composition API. Можете открыть и сравнить синтаксис, если кому интересно.

## Документация

Если вы заинтересовались Vue, вам пригодится документация:

- [устаревшая (но более приятная глазу) официальная версия](https://v3.ru.vuejs.org)
- [обновлённая официальная версия](https://ru.vuejs.org)
- [мой вариант перевода документации](https://vuejs.dragomano.ru)

## Заключение

Итак, мы закончили наше простое приложение **TODO** на Vue.js:

- успешно мигрировали с Alpine.js, узнав сходства и различия с Vue
- познакомились с основными директивами
- создали несколько компонентов

В [следующей части](../znakomstvo-s-populyarnymi-js-freymvorkami-chast-3/index.md) этой серии мы познакомимся с React.

---

<div class="grid cards" markdown>
[Скачать готовый проект (Vue Options API)](https://gitlab.com/dragomano/vue-todo){ .md-button .md-button--primary }

[Скачать готовый проект (Vue Composition API)](https://gitlab.com/dragomano/vue-composition-todo){ .md-button }

</div>
