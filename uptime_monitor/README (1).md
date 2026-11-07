# Uptime Monitor

A Django REST API that watches websites, checks them automatically every 5 minutes, and stores the response-time history so you can see when a site was up, down, or slow.

## Features

- Add websites to monitor
- Manual "check now" for any site
- Automatic checks for all active sites via a custom Django management command
- Stores status (UP/DOWN), HTTP status code, response time (ms), and error message for every check
- Check history per site, newest first
- Pause a site without losing its history (`is_active` flag)
- One failing site never stops the rest of the round (per-site error handling)

## Tech Stack

- Python, Django, Django REST Framework
- `requests` library for HTTP checks
- SQLite (development)
- Windows Task Scheduler for the 5-minute timer (can be swapped for cron, APScheduler, or Celery)

## How to Run

```bash
# 1. Clone and enter the project
git clone <your-repo-link>
cd <project-folder>

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Set up the database
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/sites/` | Add a site to monitor |
| GET | `/sites/` | List all sites |
| POST | `/sites/<id>/check/` | Run a check now and save the result |
| GET | `/sites/<id>/history/` | Show saved checks for a site (newest first) |
| GET	|`/sites/<id>/stats/`	|Total checks, UP checks, uptime %, average response time|

### Add a site

```http
POST /sites/
Content-Type: application/json

{ "name": "Google", "url": "https://www.google.com/" }
```

Response (201):

```json
{ "message": "site has created succefully " }
```

### Run a check

```http
POST /sites/1/check/
```

Response (201):

```json
{
  "site": 1,
  "status": "UP",
  "status_code": 200,
  "response_time_ms": 142,
  "checked_at": "2026-11-02T11:21:00Z",
  "error": ""
}
```

A site that does not answer is saved as `DOWN` with `status_code: null` and an error message.

### Get history

```http
GET /sites/1/history/
```

Returns a list of checks, newest first. Returns 404 if the site does not exist.

## How the Scheduler Works

Automatic checking is split into small pieces:

| File | Job |
|---|---|
| `monitor/test_check.py` | `check(url)` visits one website and returns status, code, and response time |
| `monitor/services.py` | `run_check(site)` calls `check` and saves a `Check` row |
| `monitor/views.py` | API views; the manual check endpoint calls `run_check` |
| `monitor/management/commands/run_checks.py` | Loops over all active sites and calls `run_check` for each |

Run one round of checks by hand:

```bash
python manage.py run_checks
```

To repeat it every 5 minutes, schedule that command with a timer. On Windows, use Task Scheduler:

- **Program/script:** full path to the venv's `python.exe`
- **Add arguments:** `manage.py run_checks`
- **Start in:** the folder that contains `manage.py`
- **Trigger:** repeat every 5 minutes, indefinitely

The scheduler calls `run_check` directly, so it does not need the web server to be running.

## Data Model

- **Site:** `name`, `url` (unique), `is_active`, `created_at`
- **Check:** `site` (foreign key), `status`, `status_code`, `response_time_ms`, `checked_at`, `error`

## Roadmap


- Uptime percentage and average response time
- Cleanup of old checks (retention policy)
- User login, so each user has their own sites
- Email / Telegram alerts when a site goes DOWN
- Public status page
- Deployment with a server-side scheduler

## Author

Built as a hands-on backend project to practice Django REST Framework, scheduling, and relational data design.
