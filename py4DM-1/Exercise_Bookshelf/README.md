# Exercise: My Bookshelf 📚

## Goal

Build a small Django website that shows a list of your favorite books, stored in the database.

This exercise uses what you learned in the Django tutorial:

- [Part 1](https://docs.djangoproject.com/en/6.1/intro/tutorial01/): projects, apps, views and URLs
- [Part 2](https://docs.djangoproject.com/en/6.1/intro/tutorial02/): models, migrations, the shell and the admin

---

## Part A: Setup

1. Create a new project called `bookshelf`:

   ```bash
   django-admin startproject bookshelf myproject
   ```

2. Go into the `myproject` folder and start the development server:

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/> and check that you see the rocket page.

3. Create an app called `books`.

---

## Part B: The model

4. In `books/models.py`, create a `Book` model with three fields:

   | Field    | Type    | Notes                    |
   |----------|---------|--------------------------|
   | `title`  | text    | max 200 characters       |
   | `author` | text    | max 100 characters       |
   | `year`   | integer | the publication year     |

5. Add a `__str__()` method that returns the book's title.

6. Add the app to `INSTALLED_APPS` in `bookshelf/settings.py`.

7. Create and apply the migrations:

   ```bash
   python manage.py makemigrations books
   python manage.py migrate
   ```

---

## Part C: Add data

8. Open the Django shell and create **at least 2 books**:

   ```bash
   python manage.py shell
   ```

9. Register the `Book` model in `books/admin.py`.

10. Create a superuser, log in at <http://127.0.0.1:8000/admin/> and add **at least 2 more books**.

---

## Part D: Show the books on a web page

11. In `books/views.py`, write an `index` view that:
    - gets all the books from the database
    - returns an HTML list using `HttpResponse`

    Each book should look like this:

    > The Hobbit by J.R.R. Tolkien (1937)

12. Create the file `books/urls.py` and connect it to `bookshelf/urls.py`, so that the page is available at:

    <http://127.0.0.1:8000/books/>

---

## ✅ You are done when...

- Visiting `/books/` shows **every book** in the database.
- If you add a new book in the admin and refresh the page, **it appears in the list**.

---

## ⭐ Bonus (if you finish early)

### Bonus 1: Use a template

Move the HTML out of the view and into a template file:

```
books/templates/books/index.html
```

Hints:

- In the view, use `render(request, "books/index.html", {"books": books})`.
- In the template, loop over the books with `{% for book in books %} ... {% endfor %}`.
- Show a value with `{{ book.title }}`.

### Bonus 2: Filter

Add a second page at `/books/old/` that shows only books published **before 2000**.

Hint: `Book.objects.filter(year__lt=2000)`

### Bonus 3: Sort

Show the books sorted by year, from oldest to newest.

Hint: `.order_by("year")`

---

## 🛠️ Common problems

| Problem | Likely cause |
|---------|--------------|
| `no such table: books_book` | You forgot `makemigrations` or `migrate`. |
| `makemigrations` says "No changes detected" | The app is missing from `INSTALLED_APPS`. |
| 404 "Page not found" | You opened `/` instead of `/books/`. |
| `Book` is not shown in the admin | You forgot to register it in `books/admin.py`. |
| `TemplateDoesNotExist` (bonus) | Check the folder name: `books/templates/books/index.html`. Restart the server after creating new folders. |
