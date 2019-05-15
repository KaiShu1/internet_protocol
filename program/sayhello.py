def app(env, start_response):
    status = b'200 OK'
    headers = b'Server: HelloServer\r\n'
    start_response(status, headers)
    return b'hello'
