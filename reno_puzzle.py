#Adrien Forkum
#Created 8/8/2020
#Python 3.6

from reno_log_err import logger
import random

class Cell(object):
	def __init__(self, board_pos, value=None, avail_vals=None):
		self.value = value
		self.board_pos = board_pos
		self.avail_vals = avail_vals
		self.nbrs = []

	def get_nbrs(self):
		return self.nbrs


class Puzzle(object):
	def __init__(self, size=None, sol_pool=False):
		self.b_size = size
		self.fix_pnts = {}
		self.board_cells = []
		self.board_points = {}
		self.start_cell = None
		self.end_cell = None
		self.sol_pool = sol_pool

	def in_bounds(self, coords):
		if coords[0] < 0 or coords[1] < 0 or coords[0] > self.b_size or coords[1] > self.b_size:
			return False
		return True

	def add_cell(self, position, num):
		"""
		Take a position tuple and create a new cell object with that point
		"""
		logger.write(f'Adding new point -> {position}')
		new_cell = Cell(position)
		new_cell.value = num
		if not self.board_cells:
			logger.write(f'Starting point -> {new_cell.board_pos}')
			self.start_cell = new_cell
		elif len(self.board_cells) is self.b_size - 1:
			logger.write(f'End point -> {new_cell.board_pos}')
			self.end_cell = new_cell
		self.board_points[position] = new_cell 
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
			if not adj_cells:
				raise ValueError('Ran out of cells.')
			logger.write("Searching for new point...")
			new_point = adj_cells[random.randint(0,len(adj_cells) - 1)]
			adj_cells.remove(new_point)

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

			if n_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[n_nbr])
			if s_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[s_nbr])
			if e_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[e_nbr])
			if w_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[w_nbr])

			if ne_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[ne_nbr])
			if se_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[se_nbr])
			if nw_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[nw_nbr])
			if sw_nbr in self.board_points.keys():
				cell.nbrs.append(self.board_points[sw_nbr])

	
	def gen_map(self):
		start_point = (random.randint(1,self.b_size), random.randint(1, self.b_size))
		self.add_cell(start_point, 1)
		old_point = start_point

		# Loop through max map size 
		for pnts_lft in range(1, self.b_size):
			new_point = self.gen_next_point(old_point)
			self.add_cell(new_point, pnts_lft + 1)
			old_point = new_point
		logger.write(f'Total map size -> {len(self.board_cells)}')
		logger.write('Finding neighbors...')
		self.find_nbrs()
		logger.write('Neighbors found')


	def reslv_pzl(self):
		"""
		Attempts to resolve the current puzzle.
		"""
		cur_sol = []
		solutions = []
		explored = []
		logger.write('Finding solutions...')
		start = self.start_cell
		for nbr in start.get_nbrs():
			self.bk_trk(nbr, [start], solutions, [start])
		
		if (len(solutions) > 2) and not self.sol_pool:
			logger.write('Too many solutions!')
		elif solutions:
			count = 1
			for solution in solutions:
				logger.write(f'Solution {str(count)}')
				logger.write([cell.value for cell in solution])
				logger.write([cell.board_pos for cell in solution])
				count += 1
			# Take solutions and find enforced points
			self.fix_pnts = self.rslv_fix_pnts(solutions)
		else:
			logger.write('No solutions found')
			logger.write(f'Last solution {[cell.value for cell in cur_sol]}')

	def bk_trk(self, c, cur_sol, solutions, explored):
		#logger.write(f'Current cell: {c.board_pos}')
		# Too many solutions check
		if len(solutions) >= 3 and not self.sol_pool:
			return
		
		# Solution = true to find next board pos
		if self.is_solution(c, solution=True, cur_sol=cur_sol):
			logger.write('Solution found!')
			cur_sol.append(c)
			solutions.append(cur_sol)
			return solutions
		# Solution = true to skip valid move check 
		elif self.valid_move(c, cur_sol, solution=True):
			cur_sol.append(c)
			explored.append(c)
		else:
			return

		# logger.write(f'Neighbors: {[n.board_pos for n in c.get_nbrs()]}')
		for nbr in c.get_nbrs():
			# if nbr not in explored:
			self.bk_trk(nbr, cur_sol.copy(), solutions, explored.copy())
	
	def is_solution(self, cell, solution=False, cur_sol=None):
		if solution:
			if cell.board_pos is self.end_cell.board_pos and len(cur_sol) == self.b_size - 1:
				return True
		elif cell.value is self.end_cell.value:
			return True
		return False

	def valid_move(self, cell, cur_sol, solution=False):
		if solution:
			if cell not in cur_sol and len(cur_sol) <= self.b_size - 1 and cell != self.end_cell:
				return True
		elif cur_sol[-1].value == (cur_sol[-1].value + 1):
			return True
		else:
			return False

	def print_board_vals(self):
		for cell in self.board_cells:
			logger.write(f'Cell: {cell.board_pos}, Value: {cell.value}')

	def rslv_fix_pnts(self, solutions):
		key_pnts = {}
		pnts_map = {}
		for sol in solutions:
			path_idx = 0
			for c in sol:
				if path_idx not in pnts_map.keys():
					pnts_map[path_idx] = {c: 1}
				elif c not in pnts_map[path_idx].keys():
					pnts_map[path_idx] = {c: 1}
				else:
					pnts_map[path_idx][c] += 1
			for idx in pnts_map[path_idx].keys():
				if pnts_map[path_idx][idx] == 1:
					key_pnts[path_idx] = idx
		return key_pnts

