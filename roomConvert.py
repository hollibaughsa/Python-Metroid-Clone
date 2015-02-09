import sys
import os.path
from struct import *

class Block:
	def __init__(self, x, y, h, w, tiles, tSet, layer, attributes):
		self.x = x
		self.y = y
		self.h = h
		self.w = w
		self.tiles = tiles
		self.tSet = tSet
		self.attributes = attributes
		self.layer = layer

def main():
	# Get the file name and make sure it's a file
	fName = ''
	if len(sys.argv) > 1:
		fName = sys.argv[1]
	else:
		fName = raw_input('Enter room file to convert: ')
	
	if os.path.exists(fName) and os.path.isfile(fName):
		loadData(fName)
	else:
		print '%s is not a file or does not exist.' % (fName,)
		
def loadData(fName):
	# Load elements from file until entire file is read
	f = open(fName, 'r')
	blocks = []
	roomAttributes = int(f.readline()[:-1])
	head = f.readline()
	while head != '':
		if head == 'block:\n':
			head = loadBlock(f, blocks)
	
	f.close()
	makeFile(fName, roomAttributes, blocks)
	
def loadBlock(f, blocks):
	# Load data for a block
	x = y = w = h = 0
	tiles = []
	tSet = 0
	attributes = layer = 0
	line = f.readline()
	line = line[:-1]
	lineList = line.split(' ')
	x = int(lineList[0])
	y = int(lineList[1])
	line = f.readline()
	line = line[:-1]
	lineList = line.split(' ')
	w = int(lineList[0])
	h = int(lineList[1])
	line = f.readline()
	line = line[:-1]
	tiles = line.split(' ')
	i = 0
	while i < len(tiles):
		tiles[i] = int(tiles[i])
		i += 1
	line = f.readline()
	line = line[:-1]
	tSet = int(line)
	line = f.readline()
	line = line[:-1]
	layer = int(line)
	line = f.readline()
	line = line[:-1]
	attributes = int(line)
	blocks.append(Block(x, y, w, h, tiles, tSet, layer, attributes))
	return f.readline()
	
def makeFile(fName, attributes, blocks):
	# Create new file with a .crm extenstion and write the converted data
	name = fName.partition('.')
	newFName = name[0] + '.crm'
	f = open(newFName, 'w')
	f.write(chr(attributes))
	for block in blocks:
		f.write(chr(0))
		f.write(pack('b', block.x))
		f.write(pack('b', block.y))
		f.write(pack('B', block.w))
		f.write(pack('B', block.h))
		for tile in block.tiles:
			f.write(pack('B', tile))
		
		f.write(pack('B', block.tSet))
		f.write(pack('B', block.layer))
		f.write(pack('h', block.attributes))
		
	f.close()	
		
if __name__ == '__main__':
	main()