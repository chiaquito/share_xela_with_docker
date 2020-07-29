import os.path

bind = '127.0.0.1:8000'
#daemon = True
pidfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gunicorn.pid')
reload = True