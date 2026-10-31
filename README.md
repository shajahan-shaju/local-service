# Local Service

A Django service booking application with customer accounts, worker accounts,
bookings, and notifications.

## Run locally

Requires Python 3.12 or newer.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

The local SQLite database and uploaded media are intentionally excluded from
Git. Create a fresh database with migrations and add worker records/images in
the Django admin after deployment.

## Deploy to PythonAnywhere

1. Create a PythonAnywhere web app using Python 3.13 and manual configuration.
2. Clone this repository into `/home/YOUR_USERNAME/Local_service` from a Bash
   console, then create a virtualenv and install `requirements.txt`.
3. In the Web tab, set the source code directory to that project folder and
   the virtualenv path to the virtualenv you created.
4. Edit the WSGI file so it loads the project's `Local_service.wsgi` module,
   with the project directory on `sys.path`.
5. In `Local_service/settings.py` environment, set `DJANGO_DEBUG=false`,
   `DJANGO_SECRET_KEY` to a private random value, and
   `DJANGO_ALLOWED_HOSTS` to `YOUR_USERNAME.pythonanywhere.com`.
6. Run `python manage.py migrate` and `python manage.py collectstatic` from
   the project directory; map the `/static/` URL to `staticfiles/` in the
   Web tab, then reload the web app.
7. Add worker records and uploaded images through the admin or application.

Never commit `.env`, `db.sqlite3`, or uploaded `media/` files.

## Deploy to Render

The repository includes a Render Blueprint (`render.yaml`) that creates a
Django web service and PostgreSQL database. Connect this GitHub repository in
Render's Blueprint flow and apply the Blueprint. Render installs dependencies,
collects static files, runs migrations, and starts Gunicorn during deployment.

After the first deploy, create an administrator from the Render Shell with
`python manage.py createsuperuser`. Uploaded media files use the web service's
local filesystem; use external object storage if uploaded files must survive
service replacement or redeployment. Render's free web services can spin down
when idle, and free PostgreSQL databases expire after 30 days, so use a paid
database for data that must persist long term.
