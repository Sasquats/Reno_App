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

	def in_bounds(self, coords):
		if coords[0] < 0 or coords[1] < 0 or coords[0] > self.b_size or coords[1] > self.b_size:
			return False
		return True

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
		adj_cells = []
		new_point = prev_point
		prev_x = prev_point[0]
		prev_y = prev_point[1]

		n_cell = (prev_x, prev_y + 1)
		ne_cell = (prev_x + 1, prev_y + 1)
		e_cell = (prev_x + 1, prev_y)
		se_cell = (prev_x + 1, prev_y - 1)
		s_cell = (prev_x, prev_y - 1)
		sw_cell = (prev_x - 1, prev_y - 1)
		w_cell = (prev_x - 1, prev_y)
		nw_cell = (prev_x - 1, prev_y + 1)
		
		# Check cells for n,s,e,w
		if self.in_bounds(n_cell):
			adj_cells.append(n_cell)
		if self.in_bounds(s_cell):
			adj_cells.append(s_cell)
		if self.in_bounds(e_cell):
			adj_cells.append(e_cell)
		if self.in_bounds(w_cell):
			adj_cells.append(w_cell)

		# Check cells for ne, nw, se, sw
		if self.in_bounds(ne_cell):
			adj_cells.append(ne_cell)
		if self.in_bounds(se_cell):
			adj_cells.append(se_cell)
		if self.in_bounds(nw_cell):
			adj_cells.append(nw_cell)
		if self.in_bounds(sw_cell):
			adj_cells.append(sw_cell)

		# Loop untill point not on board is found		
		while new_point in self.board_points:
			new_point = adj_cells[random.randint(0,len(adj_cells) - 1)]

		return new_point

	def find_nbrs(self):
		for cell in self.board_cells:
			cur_x = cell.board_pos[0]
			cur_y = cell.board_pos[1]
			n_nbr = (cur_x, cur_y + 1)
			ne_nbr = (cur_x + 1, cur_y + 1)
			e_nbr = (cur_x + 1, cur_y)
			se_nbr = (cur_x + 1, cur_y - 1)
			s_nbr = (cur_x, cur_y - 1)
			sw_nbr = (cur_x - 1, cur_y - 1)
			w_nbr = (cur_x - 1, cur_y)
			nw_nbr = (cur_x - 1, cur_y + 1)

			if n_nbr in self.board_points:
				cell.nbrs.append(n_nbr)
			if s_nbr in self.board_points:
				cell.nbrs.append(s_nbr)
			if e_nbr in self.board_points:
				cell.nbrs.append(e_nbr)
			if w_nbr in self.board_points:
				cell.nbrs.append(w_nbr)

			if ne_nbr in self.board_points:
				cell.nbrs.append(ne_nbr)
			if se_nbr in self.board_points:
				cell.nbrs.append(se_nbr)
			if nw_nbr in self.board_points:
				cell.nbrs.append(nw_nbr)
			if sw_nbr in self.board_points:
				cell.nbrs.append(sw_nbr)

	
	def gen_map(self):
		start_point = (random.randint(1,self.b_size), random.randint(1, self.b_size))
		self.add_cell(start_point)
		old_point = start_point

		# Loop through max map size 
		for pnts_lft in range(1, self.b_size):
			new_point = self.gen_next_point(old_point)
			self.add_cell(new_point)
			old_point = new_point
		logger.write(f'Total map size -> {len(self.board_cells)}')
		logger.write('Finding neighbors...')
		self.find_nbrs()
		logger.write('Neighbors found')


	def gen_puzzle(self):
		cur_sol = []
		solutions = []
		self.bk_trk(self.start_cell.board_pos, explored, solutions)
		
				
	def bk_trk(self, c, cur_sol, solutions):
		cur_sol.appned(c)
		if not self.is_solution(c):
			return False
		if self.is_solution(c):
			solutions.append(cur_sol)
		for nbr in c.get_nbrs():
			bk_trk(nbr, explored)
	
	def is_solution(self, cell):
		

class Cell(object):
	def __init__(self, board_pos, value=None, avail_vals=None):
		self.value = value
		self.board_pos = board_pos
		self.avail_vals = avail_vals
		self.nbrs = []

	def get_nbrs(self):
		return self.nbrs

