#Adrien Forkum
#Created 8/8/2020
#Python 3.6

from reno_log_err import logger
import random

class Puzzle(object):
	def __init__(self, size=None, hint_num=None):
		self.b_size = size
		self.hint_num = hint_num
		self.board_cells = []
		self.board_points = []
		self.start_cell = None
		self.end_cell = None

	def add_cell(self, position):
		"""
		Take a position tuple and create a new cell object with that point
		"""
		logger.write(f'Adding new point -> {position}')
		new_cell = Cell(position)
		if not self.board_cells:
			logger.write(f'Starting point -> {new_cell.board_pos}')
			self.start_cell = new_cell
		elif len(self.board_cells) is self.b_size - 1:
			logger.write(f'End point -> {new_cell.board_pos}')
			self.end_cell = new_cell
		self.board_points.append(position)
		self.board_cells.append(new_cell)

	def gen_next_point(self, prev_point):
		"""
		Take last created position tuple and find next not used adjacent position
		"""
		new_point = prev_point
		prev_x = prev_point[0]
		prev_y = prev_point[1]

		# Loop untill point not on board is found		
		while new_point in self.board_points:
			x_diff = random.randint(-1,1)
			y_diff = random.randint(-1,1)
			new_point = (prev_x + x_diff, prev_y + y_diff)

		return new_point

	def find_nbrs(self):
		for cell in self.board_cells:
			cur_x = cell.board_pos[0]
			cur_y = cell.board_pos[1]
			n_nbr = (cur_x, cur_y + 1)
			s_nbr = (cur_x, cur_y - 1)
			e_nbr = (cur_x + 1, cur_y)
			w_nbr = (cur_x - 1, cur_y)

			if n_nbr in self.board_points:
				cell.nbrs.append(n_nbr)
			if s_nbr in self.board_points:
				cell.nbrs.append(s_nbr)
			if e_nbr in self.board_points:
				cell.nbrs.append(e_nbr)
			if w_nbr in self.board_points:
				cell.nbrs.append(w_nbr)

	
	def gen_map(self):
		start_point = (random.randint(1,self.b_size), random.randint(1, self.b_size))
		self.add_cell(start_point)
		old_point = start_point

		for pnts_lft in range(1, self.b_size):
			new_point = self.gen_next_point(old_point)
			self.add_cell(new_point)
			old_point = new_point
		logger.write(f'Total map size -> {len(self.board_cells)}')
		logger.write('Finding neighbors...')
		self.find_nbrs()
		logger.write('Neighbors found')


	def gen_puzzle(self):
		pass
		


class Cell(object):
	def __init__(self, board_pos, value=None, avail_vals=None):
		self.value = value
		self.board_pos = board_pos
		self.avail_vals = avail_vals
		self.nbrs = []

