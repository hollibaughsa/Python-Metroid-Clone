from struct import *

def main():
	f = open('testRoom.crm', 'r')
	i = f.read(1)
	while i != '':
		print ord(i)
		i = f.read(1)
		
	f.close()
		
if __name__ == '__main__':
	main()