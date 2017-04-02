import numpy as np
from math import floor

numDecPts = 4
numEndPts = 10
decPts = []
endPts = []

class Node():
	def __init__(self):
		self.end = False
		self.start = False
		self.left = None
		self.forward = None
		self.right = None
		self.next = None
		self.previous = None
		self.name = None
		self.index = None

			
class TrackMap():
	def __init__(self):
		for i in range(numDecPts):
			decPts.append(Node())

		for i in range(numEndPts):
			endPts.append(Node())

		self.initEndPts()
		self.initDecPts()
		self.decPts = decPts
		self.endPts = endPts

	def initDecPts(self):
		for i in range(numDecPts):
			decPts[i].name = "decPts"
			decPts[i].index = i
			decPts[i].left = endPts[(i + 1) * 2 - 1]
			decPts[i].right = endPts[(i + 1) * 2]
			if i < numDecPts - 1:
				decPts[i].forward = decPts[i+1]
			else:
				decPts[i].forward = endPts[i * (numDecPts - 1)]
				

	def initEndPts(self):
		endPts[0].next = decPts[0]
		decPts[0].name = "endPts"
		decPts[0].index = 0
		endPts[numEndPts-1].next = decPts[numDecPts-1]
		endPts[numEndPts-1].name = "endPts"
		endPts[numEndPts-1].index = numEndPts-1
		for i in range(1,numEndPts-1):
			endPts[i].name = "endPts"
			endPts[i].index = i
			if i % 2 == 1:
				endPts[i].previous = decPts[int(floor(i / 2))]
			else:
				endPts[i].previous =  decPts[int(i / 2 - 1)]



def main():
	myMap = TrackMap()
	start = int(input("Where am I?\nendpointIndex# > "))
	stop = int(input("Where should I go?\nendpointIndex# > "))

	node = myMap.endPts[start]
	if start == 0:
		print("go forward")
		node = node.next
	else:
		if start == stop:
			print("already there")
			exit()

		print("go forward")
		node = node.previous

		if start % 2 == 0:
			if start < stop:
				print("rotate right")
			else:
				print("rotate left")
		else:
			if start > stop:
				print("rotate right")
			else:
				print("rotate left")
	
	while node != stop:
		if node.name == "decPts":
			ln = node.left
			rn = node.right
			fn = node.forward
			if ln.index == stop:
				print("rotate left")
				print("stop")
				break
			elif rn.index == stop:
				print("rotate right")
				print("stop")
				break
			else:
				print("go forward")
				node = node.forward
		else:
			if node.index == stop:
				print("stop")
				break
			else:
				node = node.previous

		print(node.name, node.index)

	#print("\nright: ",endPts[0].right, "\nleft: ", endPts[0].left, "\nforward: ", endPts[0].forward, "\nprevious: ", endPts[0].previous, "\nnext: ", endPts[0].next.next)

	#for ep in endPts:
	#	print(ep.next)

	#for i in range(len(decPts)):
		#print(decPts[i].left == endPts[(i + 1) * 2 - 1])



if __name__ == "__main__":
	main()
