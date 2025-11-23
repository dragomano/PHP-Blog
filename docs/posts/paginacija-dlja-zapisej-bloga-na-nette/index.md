---
title: 'Пагинация для записей блога на Nette'
description: 'Как сделать пагинацию для записей блога на фреймворке Nette.'
slug: paginacija-dlja-zapisej-bloga-na-nette
date: 2022-01-12
tags:
  - Nette
  - фреймворки
  - пагинация
---

В качестве продолжения статьи [Создание блога на Nette](../sozdanie-bloga-na-nette/index.md) реализуем пагинацию в нашем блоге на фреймворке Nette.

<!-- more -->

## Подготовка

Прежде всего переименуем класс `PostFacade` в `PostRepository`, а его метод `getPublicArticles` — в `findPublishedPosts`:

```php
<?php

namespace App\Model;

use Nette\SmartObject;
use Nette\Database\Explorer;
use Nette\Database\Table\Selection;
use DateTime;

final class PostRepository
{
	use SmartObject;

	private Explorer $database;

	public function __construct(Explorer $database)
	{
		$this->database = $database;
	}

	public function findPublishedPosts(): Selection
	{
		return $this->database
			->table('posts')
			->where('created_at < ', new DateTime)
			->order('created_at DESC');
	}
}
```

Кроме того, обновим наш `config/services.neon`:

```yaml
services:
	- App\Router\RouterFactory::createRouter
	- App\Model\PostRepository
```

## Обновление презентера

Затем внесём изменения в метод `renderDefault` в презентере `HomepagePresenter`:

```php
<?php

declare(strict_types=1);

namespace App\Presenters;

use App\Model\PostRepository;
use Nette\Application\UI\Presenter;

final class HomepagePresenter extends Presenter
{
	private PostRepository $repository;

	public function __construct(PostRepository $repository)
	{
		$this->repository = $repository;
	}

	public function renderDefault(int $page = 1): void
	{
		// Найдем опубликованные записи
		$posts = $this->repository->findPublishedPosts();

		// и их часть, ограниченную вычислением метода page, которую мы передадим в шаблон
		$lastPage = 0;
		$this->template->posts = $posts->page($page, 10, $lastPage);

		// а также необходимые данные для отображения опций пагинации
		$this->template->page = $page;
		$this->template->lastPage = $lastPage;
	}
}
```

## Обновление шаблона

Осталось добавить ссылки пагинации в шаблон `app\Presenters\templates\Homepage\default.latte`:

```html
{block content} ...

<div class="pagination">
  {if $page > 1}
  <a n:href="default, 1">Первая</a>
  &nbsp;|&nbsp;
  <a n:href="default, $page - 1">Предыдущая</a>
  &nbsp;|&nbsp; {/if} Страница {$page} из {$lastPage} {if $page < $lastPage} &nbsp;|&nbsp;
  <a n:href="default, $page + 1">Следующая</a>
  &nbsp;|&nbsp;
  <a n:href="default, $lastPage">Последняя</a>
  {/if}
</div>
```

Если вы не видите изменений на главной странице, добавьте побольше записей.

Таким образом, мы реализовали механизм пагинации без использования пагинатора.

## Материал, использованный для статьи

- [Paginating Database Results](https://doc.nette.org/en/best-practices/pagination) (English)
