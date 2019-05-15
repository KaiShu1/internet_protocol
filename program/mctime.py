import time


def app(environ, start_response):
    status = b'200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)
    return bytes(environ['name'] + '\t' + time.ctime(), 'utf-8')

