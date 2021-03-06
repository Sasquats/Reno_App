#Adrien Forkum
#Created 8/8/2020
#Python 3.6

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
	NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from reno_puzzle import Puzzle
from reno_log_err import logger

class RenoGame(Widget):
	def __init__(self):
		self.puzzle = Puzzle(size=10, sol_pool=True)
		self.puzzle.gen_map()
		self.puzzle.reslv_pzl()
		logger.write([self.puzzle.fix_pnts[k].value for k in self.puzzle.fix_pnts])

class RenoStart(App):
	def __init__(self):
		self.puzzle = None

	def build(self):
		game = RenoGame()

if __name__ == '__main__':
	r_start = RenoStart()
	r_start.build()