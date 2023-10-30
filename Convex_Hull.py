from PyQt5.QtCore import QLineF


class Node:
    def __init__(self, point):
        self.x = point.x()
        self.y = point.y()
        self.clockwise = self
        self.c_clockwise = self


class Hull:
    def __init__(self, leftMost, rightMost):
        self.leftMost = leftMost
        self.rightMost = rightMost

    # O(n)
    def createPolygon(self):
        lines = []
        currNode = self.leftMost
        backToStart = False
        # O(n)
        while not backToStart:
            # More accurately, this function is O(n - 1) because we draw n - 1 lines with n being the number of points
            nextNode = currNode.clockwise
            line = QLineF(currNode.x, currNode.y, nextNode.x, nextNode.y)
            lines.append(line)
            currNode = nextNode
            if currNode == self.leftMost:
                backToStart = True
        return lines


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )
		t1 = time.time()
		nodeList = []
		# O(n)
		for point in points:
			nodeList.append(Node(point))
		# O(nlogn)
		nodeList = sorted(nodeList, key=lambda node: node.x)
		t2 = time.time()
		t3 = time.time()
		finalHull = solveConvexHull(nodeList)
		t4 = time.time()
		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		polygon = finalHull.createPolygon()
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

# function solveConvexHull(nodeList)
#	calculate middle of list
# 	leftHull = divAndConquer(nodeList from beginning to middle)
#	rightHull = divAndConquer(nodeList from middle to end)
#	return combineHulls(leftHull, rightHull)

# O(nlogn): justification in writeup
def solveConvexHull(nodeList):
	# Calculate the middle point of the list using integer division.
	# This ensures proper indexing.
	middle = len(nodeList) // 2
	# Begin our left recursion with a call to divAndConquer on left half of list
	# O(nlogn): see divAndConquer
	leftHull = divAndConquer(nodeList[:middle])
	# Begin our right recursion with a call to divAndConquer on right half of list
	# O(nlogn): see divAndConquer
	rightHull = divAndConquer(nodeList[middle:])
	# Return the result of combining the two hulls together, which is a merged Hull
	# O(n): see combineHulls
	return combineHulls(leftHull, rightHull)

# function divAndConquer(nodeList)
#	if our list only has one element (base case)
#		create a hull with that one node
#		return that hull
#	calculate the middle of the list
# 	leftHull = divAndConquer(nodeList from beginning to middle)
#	rightHull = divAndConquer(nodeList from middle to end)
#	return combineHulls(leftHull, rightHull)
# O(nlogn)
def divAndConquer(list):
	# Our base case
	if len(list) == 1:
		# We return a hull with a single point
		return Hull(list[0], list[0])
	# Calculate the middle index as before
	middle = len(list) // 2
	# Begin left recursion
	# O(nlogn)
	leftHull = divAndConquer(list[:middle])
	# Begin right recursion
	# O(nlogn)
	rightHull = divAndConquer(list[middle:])
	# Merge the hulls together
	# O(n)
	mergedHull =  combineHulls(leftHull, rightHull)
	# Return the merged hull
	return mergedHull

# function combineHulls(leftHull, rightHull)
#	get the two nodes at ends of upper tangent with findUpperTangent()
#	get the two nodes at ends of lower tangent with findUpperTangent()
#	set upperTangentLeftNode clockwise ptr to the upperTangentRightNode
#	set upperTangentRightNode counter-clockwise ptr to the upperTangentLeftNode
#	set lowerTangentLeftNode counter-clockwise ptr to the lowerTangentRightNode
#	set lowerTangentRightNode clockwise ptr to the lowerTangentLeftNode
#	set the rightHull's left most node to the leftHull's left most node
#	return rightHull
# O(n): justification in writeup
def combineHulls(L, R):
	# Get the endpoints of the upper tangent from find_upper_tangent()
	# O(n): see find_upper_tangent()
	upTanLeft, upTanRight = findUpperTangent(L, R)
	# Get the endpoints of the lower tangent from find_lower_tangent()
	# O(n): see find_lower_tangent()
	lowTanLeft, lowTanRight = findLowerTangent(L, R)
	# Finish the merging by pointing the endpoints of the tangents
	# to each other
	# O(1): all the following lines are constant
	upTanLeft.clockwise = upTanRight
	upTanRight.c_clockwise = upTanLeft
	lowTanLeft.c_clockwise = lowTanRight
	lowTanRight.clockwise = lowTanLeft
	# Set the right hulls left most node to the leftmost node
	R.leftMost = L.leftMost
	return R

# O(n): justification in write up
# Or O(n^3): if the division algorithm takes as much time as I think
# function findUpperTangent(leftHull, rightHull)
#	set p to leftHull right most node
# 	set q to rightHull left most node
#	done = False
#	while not done:
#		done = true
#		get the slope between p and q with getSlope, call it slope
#		while slope is greater than the slope with p's counterclockwise neighbor and q
# 			set slope equal to this new value
# 			done = false
# 			set p equal to its counterclockwise neighbor
# 		while slope is less than the slope with p and q's clockwise neighbor
# 			set slope equal to this new value
# 			done = false
# 			set q equal to its clockwise neighbor
#	return the points p and q which are the endpoints of the tangent
# O(n): see writeup and comments inside
def findUpperTangent(L, R):
	# let n be the number of elements in L and R combined
	p = L.rightMost
	q = R.leftMost
	done = False
	# Loop until no changes are made to the endpoints
	# O(n): if we do each inner while once or every other, we will run this loop n times
	while not done:
		done = True
		slope = getSlope(p, q)
		# loop until left hull endpoint stops moving
		# O(n/2): half of the points are in L
		while slope > getSlope((p.c_clockwise), q):
			slope = getSlope((p.c_clockwise), q)
			done = False
			p = p.c_clockwise
		# loop until right hull endpoint stops moving
		# O(n/2): half of the points are in R
		while slope < getSlope(p, (q.clockwise)):
			slope = getSlope(p, (q.clockwise))
			done = False
			q = q.clockwise
	# return our endpoints
	return p, q

# O(n): justification in write-up
# O(n): justification in write up
# Or O(n^3): if the division algorithm takes as much time as I think
# function findLowerTangent(leftHull, rightHull)
#	set p to leftHull right most node
# 	set q to rightHull left most node
#	done = False
#	while not done:
#		done = true
#		get the slope between p and q with getSlope, call it slope
#		while slope is less than the slope with p's clockwise neighbor and q
# 			set slope equal to this new value
# 			done = false
# 			set p equal to its clockwise neighbor
# 		while slope is greater than the slope with p and q's counter-clockwise neighbor
# 			set slope equal to this new value
# 			done = false
# 			set q equal to its counter-clockwise neighbor
#	return the points p and q which are the endpoints of the tangent
# O(n): justification in writeup
def findLowerTangent(L, R):
	# let n be the number of elements in L and R combined
	p = L.rightMost
	q = R.leftMost
	done = False
	while not done:
		done = True
		slope = getSlope(p, q)
		# loop until left hull endpoint stops moving
		# O(n/2): half of the points are in L
		while slope < getSlope(p.clockwise, q):
			slope = getSlope(p.clockwise, q)
			done = False
			p = p.clockwise
		# loop until right hull endpoint stops moving
		# O(n/2): half of the points are in R
		while slope > getSlope(p, q.c_clockwise):
			slope = getSlope(p, q.c_clockwise)
			done = False
			q = q.c_clockwise
	return p, q

# function getSlope(p, q)
# 	return the slope of the line segment that connects point p and q
# O(1) because the numbers we are dividing are always the same size
# meaning this function has no variable effect on the runtime.
def getSlope(p, q):
	# simply return the formula for slope
	return (q.y - p.y) / (q.x - p.x)