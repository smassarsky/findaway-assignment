import sys
import copy

# maze_solver takes in maze_file path
# parses input
# initialize steps and forks lists
# since every maze has a solution, loops until there is a solution and len(forks) == 0
# if current position is end, checks whether to update best_solution
	# roll steps and forks back to second-to-last fork (reduces last fork next steps to [], rollback())
# makes list of possible next moves prioritizing descending: down, laterally the direction towards end, other lateral direction, up
	# rolls back if 0 next_steps
	# goes to next step if 1 next_step
	# if len(next_steps) > 1 checks forks for loop
	# no loop, adds node to forks and appends next step

def maze_solver(maze_file):
	maze, start, end = parse_input(maze_file)
	steps = [start]
	forks = []
	letters = 'abcdefghijklmnopqrstuvwxyz'
	best_solution = None
	length = 0

	# for DRY
	coords_of = {
		'down': lambda : (pos[0] + 1, pos[1]),
		'up': lambda : (pos[0] - 1, pos[1]) if pos[0] > 0 else (0, 0),
		'left': lambda : (pos[0], pos[1] - 1),
		'right': lambda : (pos[0], pos[1] + 1)
	}

	def rollback():
		# pop forks until there's a fork with a next step
		while len(forks) > 0 and len(forks[-1].next_steps) == 0:
			forks.pop()
		# if there are any forks left, pop steps until current == last fork and append next_step to steps
		if len(forks) > 0:
			while forks[-1].coords != steps[-1]:
				steps.pop()
			steps.append(forks[-1].pop_last())

	# continues until there is a solution and 0 forks remaining
	while(best_solution == None or len(forks) > 0):
		next_steps = []
		pos = steps[-1]

		if pos == end:
			if best_solution == None or len(steps) < length:
				best_solution = copy.copy(steps)
				length = len(best_solution)
				if len(forks) > 0:
					forks[-1].next_steps = []
			rollback()

		# rolls back if there is already a solution that takes fewer steps than current + minimum to end
		elif best_solution != None and len(steps) + min_steps_to_end(end, pos) >= length:
			rollback()

		else:
			# left first if end is left, else right first
			order = ['down', 'left', 'right', 'up'] if pos[1] - end[1] > 0 else ['down', 'right', 'left', 'up']
			for dir in order:
				coords = coords_of[dir]()
				if (coords != steps[-2] if len(steps) > 1 else True) and maze[coords[0]][coords[1]] == '_':
					next_steps.append(coords)

			if len(next_steps) == 0:
				rollback()
			elif len(next_steps) == 1:
				steps.append(next_steps[0])
			elif next((True for x in forks if x.coords == pos), False):
				rollback()
			else:
				forks.append(Fork(pos, next_steps))
				steps.append(forks[-1].pop_last())

	# fills in original maze with letters and returns it as a string
	for num, coordinate in enumerate(best_solution):
		maze[coordinate[0]][coordinate[1]] = letters[num]
	maze = map(lambda row: ''.join(row), maze)
	return '\n'.join(maze)

def min_steps_to_end(end, pos):
	return abs(end[0] - pos[0]) + abs(end[1] - pos[1])

class Fork:
	def __init__(self, coords, next_steps):
		self.coords = coords
		next_steps.reverse()
		self.next_steps = next_steps

	def pop_last(self):
		return self.next_steps.pop()

def parse_input(maze_file):
	# opens input file, creates 2-dimensional array to represent maze
	# returns array version of maze, start and end coordinates as tuple
	out_arr = []
	f = open(maze_file, 'r')
	for x in f:
		out_arr.append([char for char in x if char != '\n'])
	f.close()
	start = (0, out_arr[0].index('_'))
	rows = len(out_arr)
	end = (rows - 1, out_arr[rows - 1].index('_'))
	return (out_arr, start, end)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		print(maze_solver(sys.argv[1]))
	else:
		print('Usage: python solution.py <file name>')