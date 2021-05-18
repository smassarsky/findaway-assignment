import sys
import copy

letters = 'abcdefghijklmnopqrstuvwxyz'

def maze_solver(maze_file):
	# parses file at input path into 2d array
	# recursively searches for best solution
	# reformats best solution 2d array as string and returns it
	maze, start, end = parse_input(maze_file)
	solution = solution_finder(maze, start, end)[0]
	solution = map(lambda row: ''.join(row), solution)
	return '\n'.join(solution)

def solution_finder(maze, pos, end, step_count = -1):
	# recursively calls self for each possible next step
	# if multiple possible solutions found, chooses one with lowest step count
	# if no solutions returns False
	step_count += 1
	maze = copy.deepcopy(maze)
	maze[pos[0]][pos[1]] = letters[step_count % 26]
	if end == pos:
		return (maze, step_count)
	else:
		solutions = []
		#down
		if maze[pos[0] + 1][pos[1]] == '_':
			down = solution_finder(maze, (pos[0] + 1, pos[1]), end, step_count)
			if down:
				solutions.append(down)
		#left
		if maze[pos[0]][pos[1] - 1] == '_':
			left = solution_finder(maze, (pos[0], pos[1] - 1), end, step_count)
			if left:
				solutions.append(left)
		#right
		if maze[pos[0]][pos[1] + 1] == '_':
			right = solution_finder(maze, (pos[0], pos[1] + 1), end, step_count)
			if right:
				solutions.append(right)
		#up
		if maze[pos[0] - 1][pos[1]] == '_':
			up = solution_finder(maze, (pos[0] - 1, pos[1]), end, step_count)
			if up:
				solutions.append(up)

		if len(solutions) == 0:
			return False
		else:
			best_solution = None
			for x in solutions:
				if best_solution == None or best_solution[1] > x[1]:
					best_solution = x

			return best_solution

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