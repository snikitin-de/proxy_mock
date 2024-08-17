bind = "0.0.0.0:5000"
wsgi_app = "proxy_mock.wsgi:app"
worker_class = "sync"
timeout = 65
workers = 1
limit_request_line = 8190
reload = "true"
