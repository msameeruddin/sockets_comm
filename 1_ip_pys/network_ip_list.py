import os
import socket    
import multiprocessing
import subprocess
import os

class IPListDevices(object):
	def __init__(self, pool_size=255):
		self.pool_size = pool_size

	def _get_my_ip_(self):
		"""returns the ip address of a device"""
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
		s.close()
		return ip

	def _pinger_(self, jobs_q, result_q):
		"""
		Used for pinging
		:param job_q: queue
		:param results_q: queue
		:return:
		"""
		with open(os.devnull, 'w') as pipe:

			while True:
				ip = jobs_q.get()
				if ip is None:
					break
				try:
					subprocess.check_call(['ping', '-c1', ip], stdout=pipe)
					result_q.put(ip)
				except Exception as e:
					pass

	def _map_network_(self):
		"""
		Maps the network
		:param:
		:return: list of valid ip addresses
		"""
		ip_list = []

		# get my IP and compose a base like 192.168.1.xxx
		ip_parts = self._get_my_ip_().split('.')
		_ = ip_parts.pop()
		base_ip = '.'.join(ip_parts) + '.'

		# prepare the jobs and result queues
		jobs_q = multiprocessing.Queue()
		result_q = multiprocessing.Queue()

		pool = [
			multiprocessing.Process(target=self._pinger_, args=(jobs_q, result_q))
			for i in range(self.pool_size)
		]

		for p in pool:
			p.start()

		# cut the ping processes
		for i in range(1, self.pool_size):
			jobs_q.put(base_ip + '{}'.format(i))

		for p in pool:
			jobs_q.put(None)

		## time taking process
		for p in pool:
			p.join()

		while not result_q.empty():
			ip = result_q.get()
			ip_list.append(ip)

		return ip_list

	def _get_addr_hostname_(self):
		"""returns a dictionary having hostname as `key` and ip_address as `value`"""
		ip_addr_list = self._map_network_()
		host_addrs = [socket.gethostbyaddr(ip_addr) for ip_addr in ip_addr_list]
		return self._map_host_ip_(host_list=host_addrs)

	def _map_host_ip_(self, host_list):
		"""mapping method that returns a dictionary"""
		hostnames = [hip[0] for hip in host_list]

		ip_addrs = []
		for hip in host_list:
			if len(hip[2]) == 1:
				ip_addrs.append(hip[2][0])
			else:
				for i in hip[2]:
					single_addr = i.split('.')
					if single_addr[-1] != '1':
						ip_addrs.append('.'.join(single_addr))
					else:
						pass
		hostname_ipaddress = {i : j for (i, j) in zip(hostnames, ip_addrs)}

		return hostname_ipaddress







if __name__ == '__main__':
	ips = IPListDevices()
	host_addrs = ips._get_addr_hostname_()
	print(host_addrs)
