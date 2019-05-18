import sys
from socket import *
from multiprocessing import Process

STATIC_ROOT_PATH = './static'


class HTTPServer(object):
    """
    服务器建立与客户端的连接
    接收客户端的请求信息
    """

    def __init__(self, application, port=8000):
        # 创建Tcp 套接字接受客户端连接
        self.s_socket = socket(AF_INET, SOCK_STREAM)
        self.s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_socket.bind(('', port))
        self.s_socket.listen(5)
        self.app = application
        self.response_start_line = b''
        self.response_headers = b''

    def start_response(self, status, headers):
        self.response_start_line = b'HTTP/1.1 ' + status + b'\r\n'
        # WSGI规定 app传来的headers是以元组保存一组数据,整体以列表存在
        for header in headers:
            self.response_headers += header[0] + b':' + header[1] + b'\r\n'

    def handle_client(self, c_s):
        request_data = c_s.recv(1024)
        if len(request_data) > 0:
            # 对HTTP请求抽丝剥茧 选出请求页面
            request_path = str(request_data.splitlines()[0].split(b' ')[1], 'utf-8')
            if request_path.startswith('/static'):
                # 此处可以添加静态文件单独处理方法
                pass
            print(request_path)
            env = {
                'PATH_INFO': request_path,
            }
            response_body = bytes(self.app(env, self.start_response), 'utf-8')
            # 由于HTTP请求报文其 请求头和请求体 之间用空行区分
            # 在字符串类型下设置\n即换行,但在真正windows数据中是默认采用\r\n的
            response = self.response_start_line + self.response_headers + b"\r\n" + response_body
            print(response)
            c_s.send(response)
        else:
            c_s.close()

    def run(self):
        while True:
            c_socket, c_addr = self.s_socket.accept()
            print("[%s, %s]用户已连接" % c_addr)
            p = Process(target=self.handle_client, args=(c_socket,))
            p.start()
            c_socket.close()


def main():
    # 设置额外运行参数 dynamic_web_framework:app
    module_name, app = sys.argv[1].split(":")
    app = __import__(module_name).app
    s = HTTPServer(app)
    s.run()


if __name__ == "__main__":
    main()
