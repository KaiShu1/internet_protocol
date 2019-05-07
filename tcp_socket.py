from socket import *
import struct

# 小端(3 --> 0x0003，低位内存地址对应小数据) 大端(3 --> 0x3000)
# ! 表示按照网络大端方式组织
# 后面的内容可以认为是占位符的使用
# H：两个字节长度
# 8：表示后面最近内容的个数
# s：bytes 多个字节
# b：byte  1个字节
# struct.pack('!H8sb5sb', 1, )
# struct.unpack()

# 服务器端
ss = socket(AF_INET, SOCK_STREAM)
'''
1.创建套接字SOCK_STREAM
2.绑定ip和port
3.服务器端开始监听端口listen
4.等待连接accept 
    - 连接对应发送方的套接字 和 发送方ip与port
    - 注意:1.绑定的套接字用于接受新的客户端连接
          2.创建新的套接字用于连接当前客户端
5.recv/send 收发数据
6.关闭套接字
'''
s_addr = ("192.168.145.128", 7788)
ss.bind(s_addr)
# backlog 表示队列大小
ss.listen(4)
new_s, c_addr = ss.accept()

# 客户端
'''
1.创建套接字
2.connect连接服务端
3.收发数据
4.关闭套接字
'''

cs = socket(AF_INET, SOCK_STREAM)
cs.connect(s_addr)
cs.send(b'haha')

cs.close()

# 在TCP中，如果一方收到了对方的数据，其一定会发送ack确认包
# 而在UDP中，没有这个过程，所以导致tcp稳定，udp不稳定

# tcp三次握手
'''
1. syn       :客户端生成一个随机的数字发给服务器
2. ack + syn :服务器响应第一个syn数字+1 和 一个随机的数字发给客户端
3. ack       :ack称为响应包，在syn数字基础上+1
'''

