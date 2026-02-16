from vercel_wsgi import make_handler
from app import app as flask_app

# Create the WSGI handler that Vercel will invoke for requests.
handler = make_handler(flask_app)
