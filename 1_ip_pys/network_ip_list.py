import os
import socket    
import multiprocessing
import subprocess
import os

def pinger(job_q, results_q):
	
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

def get_my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

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
		multiprocessing.Process(
			target=pinger, 
			args=(jobs, results)
		) 
		for i in range(pool_size)
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

list_ip = map_network()
for i in list_ip:
	print(socket.gethostbyaddr(i))

# print(socket.gethostbyaddr('192.168.225.2'))

# if __name__ == '__main__':
# 	print('Mapping...')
# 	lst = map_network()
# 	print(lst)