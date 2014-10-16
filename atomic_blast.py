from Tkinter import *

grid_size = 600
grid_resolution = 40  # Grid dimensions = (grid_size/grid_resolution) x (grid_size/grid_resolution)

class GridNodes(object):
	"""contains data for each nodes inside grid"""
	def __init__(self, canvas, x, y):
		self.node_type = None 			# which player has his dice in the node
		self.canvas = canvas
		self.x = x
		self.y = y
		self.cap = 0
		# get neighbour
		max_grid = (grid_size/grid_resolution) - 1
		self.neighbour = []
		if x - 1 >= 0:
			self.neighbour.append([x-1,y])
			self.cap = self.cap + 1
		if x + 1 <= max_grid:
			self.neighbour.append([x+1,y])
			self.cap = self.cap + 1
		if y - 1 >= 0:
			self.neighbour.append([x,y-1])
			self.cap = self.cap + 1
		if y + 1 <= max_grid:
			self.neighbour.append([x,y+1])
			self.cap = self.cap + 1

		self.current_state = 0   # no of atoms in this node currently
		self.circles = [] 		 # circle objects to delete them

	def update(self, turn):
		# print "inside",self.x,self.y,"turn",turn
		if self.node_type == None:
			self.node_type = turn
		self.current_state = self.current_state + 1
		if self.current_state == self.cap:
			# atom blast state
			self.current_state = 0
			for each_circle in self.circles:
				self.canvas.delete(each_circle)
			self.circles = []
			# reset node ownership
			self.node_type = None
			# update neghbours recursively
			for neighbour in self.neighbour:
				# print self.x,self.y,"calls",neighbour[0],neighbour[1]
				GridNodes.nodes[neighbour[0]][neighbour[1]].update(turn)
		else:
			if self.node_type == turn or self.node_type == None:
				# Draw one more atom
				node_x_edge = int(0.05 * float(grid_resolution)) + self.x*grid_resolution + ( (self.current_state - 1) * (grid_resolution/3) ) # later term decides which number of atom to place and where to place and 5 is manual adjust ment
				node_y_edge = (self.y*grid_resolution) + ( (grid_resolution/2) - (grid_resolution/8) )# align center
				self.circles.append( self.canvas.create_oval( node_x_edge, node_y_edge, (node_x_edge)+(grid_resolution/4), (node_y_edge)+(grid_resolution/4), fill=GridNodes.colours[turn]) )
			else:
				# this is atom blast takeover, change owner
				self.node_type = turn
				# remove old owner atoms
				for each_circle in self.circles:
					self.canvas.delete(each_circle)
				self.circles = []
				# add new atoms
				for n in range(self.current_state):
					node_x_edge = int(0.05 * float(grid_resolution)) + self.x*grid_resolution + ( n * (grid_resolution/3) ) # later term decides which number of atom to place and where to place and 5 is manual adjust ment
					node_y_edge = (self.y*grid_resolution) + ( (grid_resolution/2) - (grid_resolution/8) )# align center
					self.circles.append( self.canvas.create_oval( node_x_edge, node_y_edge, (node_x_edge)+(grid_resolution/4), (node_y_edge)+(grid_resolution/4), fill=GridNodes.colours[turn]) )



class CRGrid(object):
	"""Class to initiate whole grid of the game board"""
	def __init__(self, grid_size, players):
		self.size = grid_size
		self.root = Tk()
		self.root.title("Chain Reaction")
		self.no_of_players = players
		self.current_turn = 0

		# self.firstframe = Frame(self.root)
		# self.firstframe.pack()

		self.canvas = Canvas(self.root, width=grid_size, height=grid_size, background='grey')
		self.canvas.pack()
		# Draw grid on canvas
		x = 0
		while x < grid_size:
			self.canvas.create_line(x,0,x,grid_size,fill = 'white')
			x = x + grid_resolution
		y = 0
		while y < grid_size:
			self.canvas.create_line(0,y,grid_size,y,fill = 'white')
			y = y + grid_resolution
		# Bind click event
		self.canvas.bind("<Button-1>", self.canvas_click)

		# initiate all nodes in the grid
		self.nodes = []
		for numx in range( (grid_size/grid_resolution) ):			
			for numy in range( (grid_size/grid_resolution) ):
				try:
					self.nodes[numx].append( GridNodes( self.canvas, numx, numy ) )
				except Exception, e:
					self.nodes.append( [GridNodes( self.canvas, numx, numy )] )
		# class variables for GridNodes
		GridNodes.nodes = self.nodes
		GridNodes.grid = self
		GridNodes.colours = ['red','green','blue','yellow','black','orange']
				

		self.root.geometry("1000x900")  #Set starting window size
		self.root.mainloop() 			#starts event loop of the program

	def canvas_click(self, event):
		x = event.x/grid_resolution
		y = event.y/grid_resolution
		if self.nodes[x][y].node_type == self.current_turn or self.nodes[x][y].node_type == None:
			self.nodes[x][y].update( self.current_turn )
			self.current_turn = self.get_next_turn()

	def get_next_turn(self):
		next_player = self.current_turn + 1
		if next_player < self.no_of_players:
			return next_player
		else:
			# all turn done start from first player
			return 0


if __name__ == '__main__':
	game_grid = CRGrid(grid_size, 2)

