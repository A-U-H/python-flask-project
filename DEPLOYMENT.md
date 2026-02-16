# Deployment notes

- This project uses SQLite by default (file: `instance/ecom_squire.db`). On Vercel serverless functions the filesystem is ephemeral and writes do not persist between cold starts or separate instances. For production use you should replace SQLite with a managed database (Postgres, MySQL, or a hosted DB) and update `SQLALCHEMY_DATABASE_URI` accordingly.
- A `.python-version` file has been added to lock the Python runtime to `3.10.12` to avoid Vercel defaulting to Python 3.12.
- A Vercel function entrypoint is added at `api/index.py` using `vercel-wsgi`. `requirements.txt` was updated to include `vercel-wsgi`.
