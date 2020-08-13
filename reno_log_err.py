#Adrien Forkum
#Created 8/8/2020
#Python 3.6

from datetime import datetime

class logger():
	def write(message):
		cur_time = datetime.now().time()
		with open('logging.txt', 'a') as f:
			f.write(f'{cur_time}: {message}\n')

class Custom_Err():
	pass