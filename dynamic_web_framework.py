from dynamic_web_urls import *


class Application(object):
    """"""

    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):
        path = env.get('PATH_INFO')
        for url, handler in self.urls:
            if url == path:
                # 匹配上了路由信息
                return handler(env, start_response)
        status = b'404 Not Found'
        headers = [
            (b'Server', b'Python')
        ]
        start_response(status, headers)
        return 'not found'


app = Application(urls)
'''
if __name__ == "__main__":
    app = Application(urls)
    server = HTTPServer(app)
    server.run()
'''
