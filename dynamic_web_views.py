import time


def show_ctime(env, start_response):
    status = b'200 OK'
    headers = [
        (b'Content-Type', b'text/plain'),
    ]
    start_response(status, headers)
    return time.ctime()


def say_hello(env, start_response):
    status = b'200 OK'
    headers = [
        (b'Content-Type', b'text/plain'),
    ]
    start_response(status, headers)
    return 'hello'

