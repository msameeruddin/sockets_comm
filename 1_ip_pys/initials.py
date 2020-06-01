import socket
import os
import subprocess

hostname = socket.gethostname()
# print('hostname -<', hostname)

ip_addr = socket.gethostbyname(hostname)
# print('ip address -<', ip_addr)

address_info = socket.getaddrinfo(host=hostname, port='0000')
# print(address_info)


def get_ip_4():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# s.connect(('10.255.255.255', 1))
		s.connect(('www.google.com', 1))
		ip_addr = s.getsockname()[0]
	except Exception as e:
		print(repr(e))
		ip_addr = socket.gethostbyname(socket.gethostname())
	finally:
		s.close()
	return ip_addr

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


print('IPv4 address -<', get_ip_4())
print('IPv6 address -<', get_ip_6())
print(pinger(ip_address=get_ip_4()))
