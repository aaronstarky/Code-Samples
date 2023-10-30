class PriorityQueue(object):
    """
    An Interface class that the MinHeap inherits from
    """
    def __init__(self, list_of_nodes, dist):
        self.queue = []

    # See each individual implementation for time complexity analysis
    def insert(self, node, distance_to_node):
        return None

    # See each individual implementation for time complexity analysis
    def decrease_key(self):
        return None

    # See each individual implementation for time complexity analysis
    def delete_min(self):
        return None

    # Checks to see if the queue is empty.
    # O(1)
    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False


def get_num_chi(i, n):
    i_l_chi = (i * 2) + 1
    i_r_chi = i_l_chi + 1
    chi_num = 0
    if i_l_chi < n:
        chi_num = 1
    if i_r_chi < n:
        chi_num = 2
    return chi_num, i_l_chi, i_r_chi


class MinHeap(PriorityQueue):
    """ Constructor to add all nodes to the heap
    params:
    list_of_nodes - pretty self-explanatory
    dist - a dictionary containing the distances to each node being inserted
    O(|V|): see write up
    """
    def __init__(self, list_of_nodes, dist):
        super().__init__(list_of_nodes, dist)
        self.array = []
        self.positions = {}
        i = 0
        for node in list_of_nodes:
            self.array.append([node, dist[node.node_id]])
            self.positions[node.node_id] = i
            self.bubble_up(i)
            i = i + 1

    """ Decreases the distance value of a particular node and bubbles it into proper spot
    params:
    node - the node we are changing
    distance_to_node - the new distance to the node
    O(log|V|)
    """
    def decrease_key(self, node, distance_to_node):
        i_to_node = self.positions[node.node_id]
        self.array[i_to_node][1] = distance_to_node
        self.bubble_up(i_to_node)

    """ Deletes the minimum element from the queue, and returns it.
    O(log|V|): see write up
    """
    def delete_min(self):
        # O(1)
        return_node = self.array[0][0]
        self.array[0] = self.array[-1]
        self.array.pop(-1)
        if self.empty():
            return return_node
        self.positions[self.array[0][0].node_id] = 0
        self.positions[return_node.node_id] = None
        # O(log|V|)
        self.bubble_down(0)
        return return_node

    """ For use during the insertion of nodes into the heap
    params:
    i - the index we need to begin bubbling up from
    O(log|V|): see write up
    """
    def bubble_up(self, i):
        # Base case when we are at the top of the heap
        if i == 0:
            return
        i_parent = (i-1) // 2
        par_pair = self.array[i_parent]
        chi_pair = self.array[i]
        if chi_pair[1] < par_pair[1]:
            temp = self.array[i_parent]
            self.array[i_parent] = self.array[i]
            self.array[i] = temp
            self.positions[chi_pair[0].node_id] = i_parent
            self.positions[par_pair[0].node_id] = i
            self.bubble_up(i_parent)

    """ For use during the removal of a node from the heap
    params:
    i - the index we need bubble down from
    O(log|V|): see write up
    """
    def bubble_down(self, i):
        n = len(self.array)
        chi_num, i_l_chi, i_r_chi = get_num_chi(i, n)
        if chi_num == 0:
            return
        par_pair = self.array[i]
        if chi_num == 1:
            # compare left child
            chi_pair = self.array[i_l_chi]
            if chi_pair[1] < par_pair[1]:
                # temp = par_pair
                # par_pair = chi_pair
                # chi_pair = temp
                temp = self.array[i]
                self.array[i] = self.array[i_l_chi]
                self.array[i_l_chi] = temp
                self.positions[chi_pair[0].node_id] = i
                self.positions[par_pair[0].node_id] = i_l_chi
                self.bubble_down(i_l_chi)
        if chi_num == 2:
            # get values of both left and right child
            l_chi_pair = self.array[i_l_chi]
            r_chi_pair = self.array[i_r_chi]
            smallest = par_pair
            i_small = i
            if l_chi_pair[1] < smallest[1]:
                smallest, i_small = l_chi_pair, i_l_chi
            if r_chi_pair[1] < smallest[1]:
                smallest, i_small = r_chi_pair, i_r_chi
            if smallest != par_pair:
                # temp = par_pair
                # par_pair = smallest
                # smallest = temp
                temp = self.array[i]
                self.array[i] = self.array[i_small]
                self.array[i_small] = temp
                self.positions[smallest[0].node_id] = i
                self.positions[par_pair[0].node_id] = i_small
                self.bubble_down(i_small)

    """ Checks the size of the queue and returns a boolean whether it is empty or not
    O(1): it is clear that a constant amount of work is done here
    """
    def empty(self):
        if len(self.array) == 0:
            return True
        return False
