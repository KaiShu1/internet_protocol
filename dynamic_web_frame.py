from socket import *
from multiprocessing import Process
from sys import path

STATIC_ROOT_PATH = './static'
PROGRAM_ROOT_PATH = './program'


class HTTPServer(object):
    """
    抽象化服务器代码
    运行
    处理客户端
    """

    def __init__(self, port=8000):
        # 创建Tcp 套接字接受客户端连接
        self.s_socket = socket(AF_INET, SOCK_STREAM)
        self.s_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_socket.bind(('', port))
        self.s_socket.listen(5)
        self.response_start_line = b''
        self.response_headers = b''

    def start_response(self, status, headers):
        self.response_start_line = b'HTTP/1.1 ' + status + b'\r\n'
        # WSGI规定 app传来的headers是以元组保存一组数据,整体以列表存在
        for header in headers:
            self.response_headers += bytes('%s: %s\r\n' % header, 'utf-8')

    def handle_client(self, c_s):
        request_data = c_s.recv(1024)
        if len(request_data) > 0:
            # 对HTTP请求抽丝剥茧 选出请求页面
            self.response_start_line = b'HTTP/1.1 200 OK\r\n'
            self.response_headers = b'Server: MServer\r\n'
            request_path = str(request_data.splitlines()[0].split(b' ')[1], 'utf-8')
            print(request_path)
            if "/" == request_path:
                with open(STATIC_ROOT_PATH + "/index.html", 'rb') as f:
                    response_body = f.read()
            elif ".py" == request_path[-3:]:
                path.insert(1, PROGRAM_ROOT_PATH)
                exec_pro = __import__(request_path[1:-3])
                env = {
                    'name': 'shukai',
                }
                response_body = exec_pro.app(env, self.start_response)
            else:
                try:
                    with open(STATIC_ROOT_PATH + request_path, 'rb') as f:
                        response_body = f.read()
                except FileNotFoundError:
                    response_body = b'<h1>404 File Not Found</h1>'
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
    s = HTTPServer()
    s.run()


if __name__ == "__main__":
    main()
