## Sockets

Generalization of Unix file mechanism that provides an endpoint for communication, either across a network or within a single computer.

```python
import socket
```

## Hostname

Label that is assigned to a device connected to a computer network and is used to identify the device in a various forms of electronic communication such as World Wide Web.

```python
>>> socket.gethostname()
'localhost.localdomain'
```

## IP address

Internet Protocol address mostly a numerical label assigned to each device connected to a computer network - uses IP for communication. Acts as a unique identifier for a specific machine on a particular network. It specifies a technical format of the addressing and packets scheme. It is also used to allow a virtual connection between destination and source. Allows devices talk to each other and exchange information.

The IP address of a device changes over time, it's because the IP addresses don't belong to the devices using them. They are assigned by the network to which each device is connected. Every time a device connects to a new network, it is given a new IP.

### IPv4

First version of IP. Uses 32-bit address scheme allowing to store 2^32 address > 4 billion addresses. Still it is considered the primary internet protocol and carries 94% of internet traffic.

```python
def get_ip_4():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('www.google.com', 1))
		ip_addr = s.getsockname()[0]
	except Exception as e:
		print(repr(e))
		ip_addr = socket.gethostbyname(socket.gethostname())
	finally:
		s.close()
	return ip_addr
print(get_ip_4()) # 12.244.233.165
```

**Note** - The IP address of the form `127.0.0.1` is a special-purpose IPv4 address and is called `localhost` or `loopback` address. All computers use this address as their own, but it doesn't let computers communicate with other devices as a real IP address does. The real IP address might start with `192.168.-.-`.

### IPv6

This new version is been deployed to fulfill the need for more internet addresses and fill the gaps by resolving the issues associated with IPv4. Uses 128-bit address scheme allowing 340 unidecillion unique address space. It is called as IPng (Internet Protocol next generation).

```python
>>> address_info = socket.getaddrinfo(host=socket.gethostname(), port='0000')
>>> address_info
[
	(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('::1', 0, 0, 0)),
	(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('::1', 0, 0, 0)),
	(<AddressFamily.AF_INET6: 10>, <SocketKind.SOCK_RAW: 3>, 0, '', ('::1', 0, 0, 0)),
	(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('127.0.0.1', 0)),
	(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('127.0.0.1', 0)),
	(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_RAW: 3>, 0, '', ('127.0.0.1', 0)),
]
```

```python
def get_ip_6():
	s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	try:
		s.connect(('www.google.com', 1))
		ip_addr = s.getsockname()[0]
	except Exception as e:
		print(repr(e))
		alladdr = socket.getaddrinfo(host=socket.gethostname(), port='0000')
		ip6 = filter(lambda x: x[0] == socket.AF_INET6, alladdr)
		ip_addr = list(ip6)[0][4][0]
	finally:
		s.close()
	return ip_addr
print(get_ip_6()) # 2001:0db8:0000:0000:0000:ff00:0042:7879
```

## Can we list all the IP addresses connected to one particular network?

### Very well, we can list.

