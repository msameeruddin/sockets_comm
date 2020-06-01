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

In order to check if the IP address is valid or not, it is recommended to use `ping` following the IP address. If there is an exchage of packets, it means that the IP address is a valid number. Otherwise it is not a valid one.

```python
def pinger(ip_address):
	results = []

	with open(os.devnull, 'w') as DEVNULL:
		try:
			subprocess.check_call(['ping', '-c1', ip_address], stdout=DEVNULL)
			results.append(ip_address)
		except:
			pass

	if results:
		return True
	return False
```

```python
>>> pinger(ip_address=get_ip_4())
True
>>> pinger(ip_address='12.244.233.165')
False
```

## Can we list all the IP addresses connected to one particular network?

### Very well.

**Note** - The following method lists all `IPv4` addresses of the devices connected to a particluar network.

```python
def get_my_ip():
	## AF_NET is used for getting IPv4
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip
```

This will return the working device IPv4 address. It is needed to map all the devices of a particlular network.

```sh
➜  ~ ping -help             
Usage: ping [-aAbBdDfhLnOqrRUvV64] [-c count] [-i interval] [-I interface]
            [-m mark] [-M pmtudisc_option] [-l preload] [-p pattern] [-Q tos]
            [-s packetsize] [-S sndbuf] [-t ttl] [-T timestamp_option]
            [-w deadline] [-W timeout] [hop1 ...] destination
Usage: ping -6 [-aAbBdDfhLnOqrRUvV] [-c count] [-i interval] [-I interface]
             [-l preload] [-m mark] [-M pmtudisc_option]
             [-N nodeinfo_option] [-p pattern] [-Q tclass] [-s packetsize]
             [-S sndbuf] [-t ttl] [-T timestamp_option] [-w deadline]
             [-W timeout] destination
```

```python
import os
import subprocess

def pinger(job_q, results_q):
	"""
	Used for pinging
	:param job_q: queue
	:param results_q: queue
	:return:
	"""
	with open(os.devnull, 'w') as DEVNULL:
		while True:
			ip = job_q.get()
			if ip is None:
				break
			try:
				subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)
				results_q.put(ip)
			except:
				pass
```

The above method is used to check if the IP address is valid or not. The process is called pinging and it is used to check if a particular host is reachable. It sends data packet to a server and if it receives a data packet back, then you have a connection and this method is called as Internet Control Message Protocol (ICMP).

```python
import multiprocessing

def map_network(pool_size=255):
	"""
	Maps the network
	:param pool_size: amount of parallel ping processes
	:return: list of valid ip addresses
	"""
	ip_list = []

	# get my IP and compose a base like 192.168.1.xxx
	ip_parts = get_my_ip().split('.')
	_ = ip_parts.pop()
	base_ip = '.'.join(ip_parts) + '.'

	# prepare the jobs queue
	jobs = multiprocessing.Queue()
	results = multiprocessing.Queue()

	pool = [
		multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)
	]

	for p in pool:
		p.start()

	# cut the ping processes
	for i in range(1, pool_size):
		jobs.put(base_ip + '{}'.format(i))

	for p in pool:
		jobs.put(None)

	## takes a bit of time
	for p in pool:
		p.join()

	# collect the results
	while not results.empty():
		ip = results.get()
		ip_list.append(ip)

	return ip_list
```

Two multiprocessing queues are being used to hold the list of IP addresses shown within the network that is connected. It follows parallel ping process (used to check if the multiple hosts are up or down). It returns a list of addresses connected to a single network.

```sh
➜  ~ fping www.google.com www.amazon.com
www.google.com is alive
www.amazon.com is alive
```

It is also very easily possible to get the hostnames pertaining to the list of IP addresses. It can be easily obtained using socket.

```python
>>> list_ip = map_network()
>>> for i in list_ip:
... 	print(socket.gethostbyaddr(i))
...
('dummy.domainname', [], ['000.000.00.00'])
('dummy.domainname', [], ['000.000.00.00'])
('dummy.domainname', [], ['000.000.00.00'])
...
('dummy.domainname', [], ['000.000.00.00'])
```

### Credits
 * Stackoverflow question -> https://bit.ly/2XLZWbb
 * Sockets -> https://docs.python.org/3/library/socket.html
