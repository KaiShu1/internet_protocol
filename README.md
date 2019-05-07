# internet_protocol
TCP UDP etc

# TCP与UDP
- 优缺点: 稳定与不稳定，速度快与慢（这点并不明显）
  - 在TCP中，如果一方收到了对方的数据，其一定会发送ack确认包
  - 而在UDP中，没有这个过程，所以导致tcp稳定，udp不稳定

- UDP是写信的模型，而TCP是打电话的模型
- UDP	需要每次发送数据都需要确认 ip 和 port 来发送数据
- TCP	不需要每次都创建一个 socket，而是通过 accept 与 connect来建立二者之间的连接

## tcp三次握手 --- hello
1. syn       :客户端生成一个随机的数字发给服务器
2. ack + syn :服务器响应第一个syn数字+1 和 一个随机的数字发给客户端
3. ack       :ack称为响应包，在syn数字基础上+1

## tcp四次挥手 --- bye
1. FIN      :通常浏览器发完数据后关闭套接字close() 后，发送数据包
2. ack      :服务器收到后返回一个ack确收包，但此时二者之间套接字还没有关闭
3. FIN      :服务器调用close() 同样发送该包
4. ack      :客户端收到后返回一个ack确认包，此时套接字真正关闭

## tcp长连接和短连接
- 如看视频(长)与简单的博客网站(短)
    - 建立连接 数据传输 ... 数据传输 关闭连接  (需要注意的是由于长连接占用计算机资源，当用户长时间无操作时自动断开)
        - 优点：省去较多TCP三次握手的时间
    - 建立连接 数据传输 关闭连接 ... 建立连接 数据传输 关闭连接

## tcp十种状态
1. Listen
2. SYN_sent
3. Accept
4. established
*上为建立连接，下为关闭连接*
5. FIN_wait1
6. close_wait
7. FIN_wait2
8. last_syn
9. time_wait
10. closed
**注意对照tcp三次握手和四次挥手**