# Aura

A Django-based fitness coaching platform for managing clients, workouts, and routines.

## Tech Stack

- **Backend**: Django 6.0, Django Ninja
- **Frontend**: Tailwind CSS 4, HTMX
- **Database**: SQLite (development)

## Apps

| App        | Purpose                                 |
|------------|-----------------------------------------|
| `user`     | Custom authentication                   |
| `coach`    | Coach dashboard & clients               |
| `workouts` | Workout & routine management (REST API) |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
python manage.py migrate
python manage.py runserver
```

Build Tailwind (watch mode for development):

```bash
npm run watch
```

Build once:

```bash
npm run build
```

## Static Files

- `static/src/input.css` — Tailwind source
- `static/src/output.css` — Compiled Tailwind (gitignored)
- `static/CACHE/` — django-compressor cache (gitignored)