import time


def app(environ, start_response):
    start_response()
    return time.ctime()

