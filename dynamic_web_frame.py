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

    def start_response(self):
        pass

    def handle_client(self, c_s):
        request_data = c_s.recv(1024)
        if len(request_data) > 0:
            # 对HTTP请求抽丝剥茧 选出请求页面
            response_start_line = bytes("HTTP/1.1 200 OK\r\n", 'utf-8')
            response_headers = bytes("Server: MServer\r\n", 'utf-8')
            request_path = str(request_data.splitlines()[0].split(b' ')[1], 'utf-8')
            print(request_path)
            # response_body = ''

            if "/" == request_path:
                with open(STATIC_ROOT_PATH + "/index.html", 'rb') as f:
                    response_body = f.read()
            elif ".py" == request_path[-3:]:
                path.insert(1, PROGRAM_ROOT_PATH)
                exec_pro = __import__(request_path[1:-3])
                response_body = bytes(exec_pro.app({}, self.start_response), 'utf-8')
            else:
                try:
                    with open(STATIC_ROOT_PATH + request_path, 'rb') as f:
                        response_body = f.read()
                except FileNotFoundError:
                    response_body = b'<h1>404 File Not Found</h1>'

            # 由于HTTP请求报文其 请求头和请求体 之间用空行区分
            # 在字符串类型下设置\n即换行,但在真正windows数据中是默认采用\r\n的
            response = response_start_line + response_headers + b"\r\n" + response_body
            print(response)
            c_s.send(response)

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
