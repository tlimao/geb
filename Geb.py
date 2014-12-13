# -*- coding: utf-8 -*-
from sys import argv 
from random import randint
import os
import copy

class Geb():
	
	def __init__(self):
		print "Geb Created"
		
	def createMap(self, width, height, max_cells, min_cells, max_cell_length, min_cell_length):
		return self.__drawWalls(self.__findCells(self.__createCells(width, height, max_cells, min_cells, max_cell_length, min_cell_length),width,height),width,height)
		
	def __createCells(self, width, height, max_cells, min_cells, max_cell_length, min_cell_length):
		world = [[' ' for i in range(width)] for j in range(height)]
		
		# draw map margins
		for j in range(width):
			world[0][j] = '.'
			world[height-1][j] = '.'
		
		for i in range(height):
			world[i][0] = '.'
			world[i][width-1] = '.'
		
		# Generate random cells
		for i in range(randint(min_cells, max_cells)):
			cell_width = randint(min_cell_length, max_cell_length)
			cell_height = randint(min_cell_length, max_cell_length)
			
			start_cell_i = randint(1, width - cell_width - 1)
			start_cell_j = randint(1, height - cell_height - 1)
			
			for j in range(cell_height):
				world[start_cell_j + j][start_cell_i: start_cell_i + cell_width - 1] = ['#' for n in range(cell_width - 1)]

		return world
	
	def __findCells(self, map, width, height):
		cells = []
		# Identify all cells
		for i in range(height):
			for j in range(width):
				if map[i][j] == '#':
					map[i][j] = '*'
					neighbors = self.__findNeighbors4(i, j, width, height)
					new_cell = [[i,j]]
					
					while len(neighbors) > 0:
						neighbor = neighbors.pop()
						if map[neighbor[0]][neighbor[1]] == '#':
							new_cell.append(neighbor)
							map[neighbor[0]][neighbor[1]] = '*'
							new_neighbors = self.__findNeighbors4(neighbor[0], neighbor[1], width, height)
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
				map[i][start_j-1] = '*'
				map[i][start_j] = '*'
				map[i][start_j+1] = '*'
				
			start_i = min_i
			
			if c1[0] > c2[0]:
				start_i = max_i
			
			for j in range(min_j, max_j+1):
				map[start_i-1][j] = '*'
				map[start_i][j] = '*'
				map[start_i+1][j] = '*'
		
		return map
		
	def __findNeighbors4(self, i, j, w, h):
		neighbors = []
		
		if i - 1 >= 0: neighbors.append([i-1,j])
		if i + 1 < h: neighbors.append([i+1,j])
		if j - 1 >= 0: neighbors.append([i,j-1])
		if j + 1 < w: neighbors.append([i,j+1])
		
		return neighbors
		
	def __findNeighbors8(self, i, j, w, h):
		neighbors = []
		
		if i - 1 >= 0:
			neighbors.append([i-1,j])
			
			if j - 1 >= 0: neighbors.append([i-1,j-1])
			if j + 1 < w: neighbors.append([i-1,j+1])
			
		if i + 1 < h:
			neighbors.append([i+1,j])
			
			if j - 1 >= 0: neighbors.append([i+1,j-1])
			if j + 1 < w: neighbors.append([i+1,j+1])
			
		if j - 1 >= 0: neighbors.append([i,j-1])
		if j + 1 < w: neighbors.append([i,j+1])
		
		return neighbors
		
	def __drawWalls(self, map, width, height):
		walls = []
		for i in range(height):
			for j in range(width):
				if map[i][j] == "*":
					neighbors = self.__findNeighbors4(i, j, width, height)
					count = 0
					for neighbor in neighbors:
						if map[neighbor[0]][neighbor[1]] == '*':
							count += 1
					if count != 4:
						walls.append([i,j])
		
		for wall in walls:
			map[wall[0]][wall[1]] = '#'
		
		return map
		
	def printMap(self, map):
		for row in map:
			for element in row:
				print element,

			print
	
geb = Geb()

os.system('cls')

mi = geb.createMap(40,1000,80,20,10,6)

geb.printMap(mi)

raw_input()