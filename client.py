
import socket
import select
import pytun
import base64
import dns.message
import dns.name
import dns.query
import dns.resolver
import time

tun = pytun.TunTapDevice(
            name='client_tun', flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
tun.addr = '10.10.10.1'
tun.netmask = '255.255.255.0'
tun.mtu = 160
tun.up()

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_dns_server = ('120.78.166.34', 53)


def encode_query(tun_data: bytes):
    domain = 'group-15.cs305.fun'
    data = base64.urlsafe_b64encode(tun_data)

    # str1.str2.str3.str4.group-15.cs305.fun
    data_seq = [str(data[i:i + 63], encoding='ascii')
                    for i in range(0, len(data), 63)]
    data_seq.append(domain)
    target_domain = '.'.join(data_seq)

    name = dns.name.from_text(target_domain)
    query = dns.message.make_query(name, 'TXT')
    return query.to_wire()


def decode_response(response: bytes):
    response = dns.message.from_wire(response)
    if response.answer:
        txt_record = response.answer[0]
        ip_response = base64.urlsafe_b64decode(str(txt_record.items[0]))
    else:
        ip_response = b''
    return ip_response


def run():
    r = [tun, socket]
    w = []
    e = []
    write_to_tun_data = b''
    send_to_socket_data = b''
    timer = time.time()
    while True:
        readable, writable, exceptional = select.select(r, w, e)

        if tun in readable:
            send_to_socket_data = tun.read(tun.mtu)
        if socket in readable:
            write_to_tun_data, target_addr = socket.recvfrom(65532)
            write_to_tun_data = decode_response(write_to_tun_data)

        if tun in writable:
            tun.write(write_to_tun_data)
            write_to_tun_data = b''
        if socket in writable:
            socket.sendto(encode_query(send_to_socket_data), local_dns_server)
            send_to_socket_data = b''

        r = []
        w = []
        if write_to_tun_data:
            w.append(tun)
        else:
            r.append(socket)
        if not send_to_socket_data:
            r.append(tun)
        now = time.time()
        if now - timer > 0.4 or send_to_socket_data:
            w.append(socket)
            timer = now


if __name__ == '__main__':
    run()




