import sys
import os.path
from struct import *
from mainClasses import Block

def loadArea(fName):
	areaData = {}
	if os.path.exists(fName) and os.path.isfile(fName):
		areaData = loadAData(fName)
	else:
		print "%s is not a file or doesn't exist." (fName,)
		
	return areaData
	
def loadAData(fName):
	Data = {}
	try:
		f = open(fName, 'r')
	except:
		print "ERROR - Area file %s could not be opened" (fName,)
		return {}
	
	Data['Name'] = f.readline()[:-1]
	Data['Music'] = f.readline()[:-1]
	Data['tSet'] = f.readline()[:-1]
	f.close()
	return Data

def loadRoom(fName):
	Room = {}
	if os.path.exists(fName) and os.path.isfile(fName):
		Room = loadData(fName)
	else:
		print "%s is not a file or doesn't exist." (fName,)
	
	return Room
		
def loadData(fName):
	Room = {'Attributes':0, 'Blocks':[], 'Entities':[], 'Doors':[], \
	'Items':[], 'Elevators':[]}
	try:
		f = open(fName, 'r')
	except:
		print "ERROR - Room %s file could not be opened" (fName,)
		return {}
	Room['Attributes'] = ord(f.read(1))
	head = f.read(1)
	while head != '':
		if head == chr(0):
			head = loadBlock(f, Room)
	
	f.close()
	return Room
			
def loadBlock(f, Room):
	x = unpack('b', f.read(1))[0] * 8
	y = unpack('b', f.read(1))[0] * 8
	h = unpack('B', f.read(1))[0]
	w = unpack('B', f.read(1))[0]
	tCount = w * h
	tiles = []
	while tCount > 0:
		tiles.append(unpack('B', f.read(1))[0])
		tCount -= 1
	
	tSet = unpack('B', f.read(1))[0]
	layer = unpack('B', f.read(1))[0]
	attributes = unpack('h', f.read(2))[0]
	
	Room["Blocks"].append(Block(x, y, w, h, tiles, tSet, layer, attributes))
	
	return f.read(1)