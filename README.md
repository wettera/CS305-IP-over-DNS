# IP over DNS

## Introduction

In this project, we set up a DNS tunnel for IP packets. The final goal of such an approach is to provide full IP connectivity with only the ability to send recursives DNS queries through a local DNS resolver. The idea is to use a virtual TUN interface between the client and the server, and set a correct routing configuration on both computers. We also have to encode the IPpackets into DNS queries and answers and decode it on the other side. Then, on the server side, we need to set up a forwarding mechanism via NAT.

## Requirement

Operating system：`Ubuntu >= 16.04`

Python version：`>= 3.6`

Support `TUN/TAP`

`root` or `administrator`



## How to run

1. use the command `sudo python3 server.py` and `sudo python3 client.py` to start the program of the client and the server

      ![1](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/1.png)

​          ![2](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/2.png)

2. open another view on putty and use the command `ping 10.10.10.2`  on the client side and `ping 10.10.10.1` on the server side to test whether the connection is build. The results are as follow.

    ​       ![3](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/3.png)
    
    ![4](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/4.png)

3. use the command `ssh -i cs305dnspro_cn.pem -D 10.10.10.1:8048 ubuntu@10.10.10.2 ` to set the proxy on the client side.

   ![5](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/5.png)

4. Use the tunnel for internet access at client:

    command: `curl http://pv.sohu.com/cityjson`

   ![6](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/6.png)

​        

​        command:`curl http://www.net.cn/static/customercare/yourip.asp`

​           ![7](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/7.png)

​     

​        command:`curl https://ip.900cha.com/`

​      ![8](https://github.com/wettera/CS305-IP-over-DNS/blob/master/command_screenshot/8.png)

