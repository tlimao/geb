# -*- coding: utf-8 -*-
from sys import argv 
from random import randint
import os

max_cell_length = 10
min_cell_length = 5

max_cell_num = 8
min_cell_num = 4

class Geb():
	
	def __init__(self):
		print "Geb Created"
		
	def createCells(self, width, height):
		world = [[' ' for i in range(width)] for j in range(height)]
		
		# draw map margins
		for j in range(width):
			world[0][j] = '#'
			world[height-1][j] = '#'
		
		for i in range(height):
			world[i][0] = '#'
			world[i][width-1] = '#'
		
		# Generate random cells
		for i in range(randint(min_cell_num, max_cell_num)):
			cell_width = randint(min_cell_length, max_cell_length)
			cell_height = randint(min_cell_length, max_cell_length)
			
			start_cell_i = randint(1, width - cell_width - 1)
			start_cell_j = randint(1, height - cell_height - 1)
			
			for j in range(cell_height):
				world[start_cell_j + j][start_cell_i: start_cell_i + cell_width - 1] = ['*' for n in range(cell_width - 1)]
			
		return world
	
	def findCells(self, map, width, height):
		current_cell = 0
		cells = []
		# Identify all cells
		for i in range(width):
			for j in range(height):
				if map[i][j] == '*':
					current_cell += 1
					map[i][j] = current_cell
					neighbors = self.__findNeighbors(i, j, width, height)
					new_cell = [[i,j]]
					
					while len(neighbors) > 0:
						neighbor = neighbors.pop()
						if map[neighbor[0]][neighbor[1]] == '*':
							new_cell.append(neighbor)
							map[neighbor[0]][neighbor[1]] = current_cell
							new_neighbors = self.__findNeighbors(neighbor[0], neighbor[1], width, height)
							for new_neighbor in new_neighbors:
								if new_neighbor not in neighbors:
									neighbors.append(new_neighbor)
					
					cells.append(new_cell)
		
		# Find centers of cells
		cells_centers = []
		for cell in cells:
			center = [0, 0]
			
			for element in cell:
				center[0] += element[0]
				center[1] += element[1]
				
			center[0] /= len(cell)
			center[1] /= len(cell)
			
			center[0] = int(center[0])
			center[1] = int(center[1])

			cells_centers.append(center)

		# Draw plus simbol in center of cells
		for center in cells_centers:
			map[center[0]][center[1]] = '+'
		
		# Conect randomically all cells
		for idx in range(len(cells_centers) - 1):
			c1 = cells_centers[idx]
			c2 = cells_centers[idx+1]
			
			min_i = min(c1[0],c2[0])
			min_j = min(c1[1],c2[1])	
			max_i = max(c1[0],c2[0])
			max_j = max(c1[1],c2[1])
			
			start_j = min_j
			
			if c1[1] < c2[1]:
				start_j = max_j
			
			for i in range(min_i, max_i+1):
				map[i][start_j] = '*'
				
			start_i = min_i
			
			if c1[0] > c2[0]:
				start_i = max_i
			
			for j in range(min_j, max_j+1):
				map[start_i][j] = '-'
				
		return map
		
	def __findNeighbors(self, i, j, w, h):
		neighbors = []
		
		if i - 1 >= 0: neighbors.append([i-1,j])
		if i + 1 < w: neighbors.append([i+1,j])
		if j - 1 >= 0: neighbors.append([i,j-1])
		if j + 1 < h: neighbors.append([i,j+1])
		
		return neighbors
		
geb = Geb()

world = geb.findCells(geb.createCells(40, 40), 40, 40)

os.system('cls')

for row in world:
	for element in row:
		print element,
	
	print

raw_input()