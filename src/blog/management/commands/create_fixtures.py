from __future__ import annotations

import random
import string
from datetime import timedelta
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from ...models import Post


class Command(BaseCommand):
    help = "Create blog post fixtures with interesting content in both languages"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of quality posts to create (default: 10)",
        )
        parser.add_argument(
            "--bulk",
            type=int,
            default=0,
            help="Number of bulk/lorem ipsum posts to create (default: 0)",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed for slug generation. Use different seeds to create unique slugs (default: random)",
        )

    def handle(self, *args: object, **options: dict[str, object]) -> None:
        quality_count = int(options["count"])
        bulk_count = int(options["bulk"])
        seed = options.get("seed")

        # Initialize random seed if provided
        if seed is not None:
            random.seed(seed)
            self.stdout.write(f"Using random seed: {seed}")

        self.stdout.write(f"Creating {quality_count} quality posts...")
        self._create_quality_posts(quality_count, seed)

        if bulk_count > 0:
            self.stdout.write(f"Creating {bulk_count} bulk posts...")
            self._create_bulk_posts(bulk_count, seed)

        self.stdout.write(self.style.SUCCESS("Fixtures created successfully!"))

    def _randomize_slug(self, base_slug: str, seed: int | None) -> str:
        """Add a random suffix to the slug to make it unique."""
        if seed is None:
            # Generate a random 6-character suffix
            suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
        else:
            # Use seed-based randomization for reproducibility
            # Create a deterministic suffix based on the base slug and seed
            # Create a deterministic integer seed from seed and base_slug
            # Use a simple polynomial hash for consistency
            slug_hash = sum(ord(c) * (i + 1) for i, c in enumerate(base_slug))
            deterministic_seed = seed + slug_hash
            temp_rng = random.Random(deterministic_seed)
            suffix = "".join(
                temp_rng.choices(string.ascii_lowercase + string.digits, k=6)
            )
        return f"{base_slug}-{suffix}"

    def _create_quality_posts(self, count: int, seed: int | None) -> None:
        """Create interesting, well-written posts in both languages."""
        posts_data = [
            {
                "title_en": "Getting Started with TypeScript",
                "title_uk": "Початок роботи з TypeScript",
                "slug_en": "getting-started-with-typescript",
                "slug_uk": "pochatok-roboty-z-typescript",
                "content_en": """# Getting Started with TypeScript

TypeScript is a powerful superset of JavaScript that adds static type checking to your code. In this post, we'll explore the basics of TypeScript and how it can improve your development workflow.

## Why TypeScript?

TypeScript offers several advantages:

- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: Enhanced autocomplete and refactoring
- **Improved Code Quality**: Self-documenting code through types

## Basic Example

```typescript
function greet(name: string): string {
  return `Hello, ${name}!`;
}
```

Start using TypeScript today and see the difference it makes!""",
                "content_uk": """# Початок роботи з TypeScript

TypeScript — це потужне розширення JavaScript, яке додає статичну перевірку типів до вашого коду. У цій статті ми дослідимо основи TypeScript та як він може покращити ваш робочий процес розробки.

## Чому TypeScript?

TypeScript пропонує кілька переваг:

- **Безпека типів**: Виявлення помилок під час компіляції
- **Краща підтримка IDE**: Покращене автодоповнення та рефакторинг
- **Покращена якість коду**: Самодокументований код через типи

## Базовий приклад

```typescript
function greet(name: string): string {
  return `Привіт, ${name}!`;
}
```

Почніть використовувати TypeScript сьогодні та побачте різницю!""",
            },
            {
                "title_en": "Understanding Django ORM",
                "title_uk": "Розуміння Django ORM",
                "slug_en": "understanding-django-orm",
                "slug_uk": "rozuminnia-django-orm",
                "content_en": """# Understanding Django ORM

Django's Object-Relational Mapping (ORM) is one of its most powerful features. It allows you to interact with your database using Python code instead of SQL.

## Key Concepts

The ORM provides:

1. **Models**: Define your database structure
2. **QuerySets**: Build complex database queries
3. **Migrations**: Manage database schema changes

## Example Query

```python
from blog.models import Post

# Get all published posts
posts = Post.public.published()

# Filter by date
recent = posts.filter(published_at__gte=timezone.now() - timedelta(days=7))
```

Master the ORM to write efficient, maintainable Django applications.""",
                "content_uk": """# Розуміння Django ORM

Об'єктно-реляційне відображення (ORM) Django — одна з найпотужніших його функцій. Воно дозволяє взаємодіяти з базою даних, використовуючи код Python замість SQL.

## Ключові концепції

ORM надає:

1. **Моделі**: Визначають структуру вашої бази даних
2. **QuerySets**: Побудова складних запитів до бази даних
3. **Міграції**: Управління змінами схеми бази даних

## Приклад запиту

```python
from blog.models import Post

# Отримати всі опубліковані пости
posts = Post.public.published()

# Фільтр за датою
recent = posts.filter(published_at__gte=timezone.now() - timedelta(days=7))
```

Опануйте ORM, щоб писати ефективні, підтримувані додатки Django.""",
            },
            {
                "title_en": "CSS Custom Properties Deep Dive",
                "title_uk": "Поглиблений огляд CSS Custom Properties",
                "slug_en": "css-custom-properties-deep-dive",
                "slug_uk": "pohlyblenyi-ohliad-css-custom-properties",
                "content_en": """# CSS Custom Properties Deep Dive

CSS custom properties (variables) revolutionize how we write maintainable stylesheets. They enable dynamic theming, runtime value changes, and better code organization.

## Benefits

- **Dynamic Theming**: Change entire color schemes with one variable
- **Runtime Updates**: Modify values with JavaScript
- **Scoping**: Variables can be scoped to specific elements

## Example

```css
:root {
  --primary-color: #1e66f5;
  --spacing-unit: 1rem;
}

.button {
  background: var(--primary-color);
  padding: var(--spacing-unit);
}
```

Custom properties are the foundation of modern CSS architecture.""",
                "content_uk": """# Поглиблений огляд CSS Custom Properties

CSS custom properties (змінні) революціонізують те, як ми пишемо підтримувані таблиці стилів. Вони дозволяють динамічне темування, зміну значень під час виконання та кращу організацію коду.

## Переваги

- **Динамічне темування**: Зміна всієї кольорової схеми однією змінною
- **Оновлення під час виконання**: Зміна значень за допомогою JavaScript
- **Область видимості**: Змінні можуть бути обмежені конкретними елементами

## Приклад

```css
:root {
  --primary-color: #1e66f5;
  --spacing-unit: 1rem;
}

.button {
  background: var(--primary-color);
  padding: var(--spacing-unit);
}
```

Custom properties є основою сучасної архітектури CSS.""",
            },
            {
                "title_en": "Building a REST API with Django REST Framework",
                "title_uk": "Побудова REST API з Django REST Framework",
                "slug_en": "building-rest-api-django-rest-framework",
                "slug_uk": "pobudova-rest-api-django-rest-framework",
                "content_en": """# Building a REST API with Django REST Framework

Django REST Framework (DRF) makes it easy to build powerful, flexible REST APIs. Let's explore the core concepts.

## Serializers

Serializers convert complex data types to JSON and back:

```python
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_at']
```

## ViewSets

ViewSets combine the logic for multiple related views:

```python
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.public.published()
    serializer_class = PostSerializer
```

DRF provides everything you need for modern API development.""",
                "content_uk": """# Побудова REST API з Django REST Framework

Django REST Framework (DRF) спрощує створення потужних, гнучких REST API. Дослідимо основні концепції.

## Serializers

Serializers перетворюють складні типи даних у JSON і назад:

```python
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_at']
```

## ViewSets

ViewSets об'єднують логіку для кількох пов'язаних представлень:

```python
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.public.published()
    serializer_class = PostSerializer
```

DRF надає все необхідне для сучасного розробки API.""",
            },
            {
                "title_en": "Modern JavaScript: Async/Await Patterns",
                "title_uk": "Сучасний JavaScript: Патерни Async/Await",
                "slug_en": "modern-javascript-async-await-patterns",
                "slug_uk": "suchasnyi-javascript-paterny-async-await",
                "content_en": """# Modern JavaScript: Async/Await Patterns

Async/await syntax makes asynchronous code more readable and maintainable. Let's explore best practices.

## Basic Usage

```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/posts');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

## Parallel Execution

Execute multiple async operations in parallel:

```javascript
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);
```

Async/await simplifies complex asynchronous workflows.""",
                "content_uk": """# Сучасний JavaScript: Патерни Async/Await

Синтаксис async/await робить асинхронний код більш читабельним та підтримуваним. Дослідимо найкращі практики.

## Базове використання

```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/posts');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Помилка:', error);
  }
}
```

## Паралельне виконання

Виконайте кілька асинхронних операцій паралельно:

```javascript
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);
```

Async/await спрощує складні асинхронні робочі процеси.""",
            },
        ]

        # Load images from tmp/ folder
        images = []
        try:
            # Find project root (go up from src/blog/management/commands/)
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent.parent.parent
            tmp_folder = project_root / "tmp"

            if tmp_folder.exists() and tmp_folder.is_dir():
                # Find all wall_*.jpg files
                image_files = sorted(tmp_folder.glob("wall_*.jpg"))
                if image_files:
                    for img_path in image_files:
                        try:
                            with open(img_path, "rb") as f:
                                image_data = f.read()
                                images.append(
                                    ContentFile(image_data, name=img_path.name)
                                )
                        except OSError:
                            # Skip files that can't be read
                            continue

            if not images:
                self.stdout.write(
                    self.style.WARNING(
                        "No images found in tmp/ folder. Posts will be created without featured images."
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Error loading images from tmp/ folder: {e}. "
                    "Posts will be created without featured images."
                )
            )

        # Create posts
        for i, post_data in enumerate(posts_data[:count]):
            # Randomly select from available images (70% chance of having an image)
            featured_image = None
            if images and random.random() > 0.3:
                featured_image = random.choice(images)

            # Randomize slugs to avoid conflicts
            slug_en = self._randomize_slug(post_data["slug_en"], seed)
            slug_uk = self._randomize_slug(post_data["slug_uk"], seed)

            post = Post.objects.create(
                title=post_data["title_en"],
                slug=slug_en,
                content=post_data["content_en"],
                title_en=post_data["title_en"],
                title_uk=post_data["title_uk"],
                slug_en=slug_en,
                slug_uk=slug_uk,
                content_en=post_data["content_en"],
                content_uk=post_data["content_uk"],
                status=Post.Status.PUBLISHED,
                published_at=timezone.now() - timedelta(days=random.randint(0, 30)),
                featured_image=featured_image,
            )
            self.stdout.write(f"  Created: {post.title}")

    def _create_bulk_posts(self, count: int, seed: int | None) -> None:
        """Create bulk posts with lorem ipsum-like content."""
        lorem_en = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident."""

        lorem_uk = """Лорем іпсум долор сіт амет, консецтетур адіпісцінг еліт. Сед до еіусмод темпор інцідідунт ут лабор ет долор магна алікуа. Ут енім ад мінім веніам, квіс ноструд ехерцітатіон улламо лаборіс.

Дуіс ауте іруре долор ін репрегендеріт ін волуптате веліт ессе ціллум долор еу фугіат нулла паріатур. Екцептеур сінт окцеакат цупідатат нон проідент."""

        for i in range(count):
            # Randomize slugs to avoid conflicts
            base_slug_en = f"bulk-post-{i+1}"
            base_slug_uk = f"masovyi-post-{i+1}"
            slug_en = self._randomize_slug(base_slug_en, seed)
            slug_uk = self._randomize_slug(base_slug_uk, seed)

            Post.objects.create(
                title=f"Bulk Post {i+1}",
                slug=slug_en,
                content=lorem_en,
                title_en=f"Bulk Post {i+1}",
                title_uk=f"Масовий пост {i+1}",
                slug_en=slug_en,
                slug_uk=slug_uk,
                content_en=lorem_en,
                content_uk=lorem_uk,
                status=Post.Status.PUBLISHED,
                published_at=timezone.now() - timedelta(days=random.randint(0, 60)),
            )
