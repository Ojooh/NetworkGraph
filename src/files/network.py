from collections import namedtuple, deque



inf = float('inf')
# defining an edge for the network
Edge = namedtuple('Edge', 'start, end, line_name, cost')

# function for making an edge connecting starting point (start) and finishing point (end) with time taken (cost)
def make_edge(start, end, line_name, cost=1):
  return Edge(start, end, line_name, int(cost))



# class defining the Graph structure
class Network:
    def __init__(self, edges):
        # This checks for wrong entry (if any)
        wrong_edges = [i for i in edges if len(i) not in [2, 4]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    # function to get a node pair
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    # function to remove an edge
    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    # function to add an edge
    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    # structure of dijkstra algorithm implementation
    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such point does not exist in the map'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        # this checks all vertices which start with the current vertex
        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        # the variable curr_dist (current distance) actually measures the time of travelling that distance
        # it is made global, beacuse we need to preset it to the users, from a different function
        global curr_dist
        curr_dist = -1
        prev_dist = -1
        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            curr_dist = max(prev_dist, distances[current_vertex]) + 1
            prev_dist = curr_dist
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path, curr_dist
