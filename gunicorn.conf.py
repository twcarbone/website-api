wsgi_app = "wsgi:app"
bind = "127.0.0.1:5000"
workers = 2

# Logging
accesslog = "./logs/gunicorn.access.log"
