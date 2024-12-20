class Vertex(object):
    start: str
    end: str
    cost: float

    def __init__(self, start: str, end: str, cost: float):
        self.start = start
        self.end = end
        self.cost = cost

    def __str__(self):
        return "{} --({})--> {}".format(self.start, self.cost, self.end)

    def __repr__(self) -> str:
        return self.__str__()


class Graph(object):
    nodes: list[str]
    vertices: list[Vertex]
    heuristics: dict[str, float]

    def __init__(self, csv_content: list[list[str]]):
        self.nodes = list()
        self.vertices = list()
        self.heuristics = dict()
        self._parse_csv(csv_content)

    def _parse_csv(self, csv_content: list[list[str]]):
        # first row, skipping first and last cell (heuristic)
        header: list[str] = csv_content[0][1:]
        self.nodes = header[:-1]
        # iterate over rows, skipping first row
        for row in csv_content[1:]:
            current_node: str = row[0]
            # iterate over cells, skipping first cell
            for i, c in enumerate(row[1:]):
                # skip empty cells
                if c == "":
                    continue
                cell_value = float(c)
                # skip -1 values
                if cell_value < 0:
                    continue

                other_node: str = header[i]
                if other_node.lower() == "heuristic":
                    self.heuristics[current_node] = cell_value
                    continue

                self.vertices.append(Vertex(current_node, other_node, cell_value))

    def __str__(self) -> str:
        s = "Graph: (\nHeuristics: {}\nVertices:\n".format(self.heuristics)
        for v in self.vertices:
            s += "{}\n".format(v)
        s += ")"
        return s

    def __repr__(self) -> str:
        return self.__str__()

    # perform greedy search on graph with given start and end node.
    # returns the path as list of vertices.
    def greedy(self, start: str, target: str) -> list[Vertex]:
        current_node = start
        path: list[Vertex] = []
        # run until we reached our target
        while current_node != target:
            # generator function, returning vertices connected to current_node
            possible_vertices = [
                vertex
                for vertex in self.vertices
                if vertex.start == current_node and vertex.end != current_node
            ]
            if len(possible_vertices) == 0:
                # we are stuck
                return None
            # greedy chooses by lowest cost
            # here by using the builtin min function with a lambda function as key function
            chosen_vertex = min(possible_vertices, key=lambda x: x.cost)

            path.append(chosen_vertex)
            current_node = chosen_vertex.end

        return path

    # perform djikstra search on graph with given start and end node.
    # returns the path as list of vertices.
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    def djikstra(self, start: str, target: str) -> list[Vertex]:
        # Initialize set of unvisited nodes
        unvisisted_set: set[str] = set(self.nodes)

        # Initialize g scores
        g_scores: dict[str, float] = {node: float("infinity") for node in self.nodes}

        # Initialize previous_vertices with none for every node
        came_from: dict[str, Vertex] = {node: None for node in self.nodes}

        # Set inital g score of start node to 0
        g_scores[start] = 0

        current_node: str = None
        while len(unvisisted_set) > 0:
            # Find the current node with the smallest g score
            current_node = None
            for node in unvisisted_set:
                if current_node is None or g_scores[node] < g_scores[current_node]:
                    current_node = node
            del node
            # If we have reached the target, reconstruct the path
            if current_node == target:
                break

            # Remove the current node from the set of unvisited nodes
            unvisisted_set.remove(current_node)

            # Update the distances and previous vertices for the neighbors
            for vertex in (v for v in self.vertices if v.start == current_node):
                neighbor = vertex.end
                g_score = g_scores[current_node] + vertex.cost
                if g_score < g_scores[neighbor]:
                    came_from[neighbor] = vertex
                    g_scores[neighbor] = g_score
                del neighbor, g_score
            del vertex

        if current_node != target:
            return None
        del current_node

        # Reconstruct the path from start to target
        path = []
        current_vertex: Vertex = came_from[target]
        while current_vertex.start != start:
            path.append(current_vertex)
            current_vertex = came_from[current_vertex.start]

        path = list(reversed(path))
        return path

    # TODO check a star for correctness
    # perform a_star search on graph with given start and end node.
    # returns the path as list of vertices.
    # https://en.wikipedia.org/wiki/A*_search_algorithm
    def a_star(self, start: str, target: str) -> list[Vertex]:
        # Initialize open set with start node
        open_set = set([start])

        # Initialize g and f scores
        g_scores: dict[str, float] = {node: float("infinity") for node in self.nodes}
        f_scores: dict[str, float] = {node: float("infinity") for node in self.nodes}

        # Dictionary to store the path
        came_from: dict[str, Vertex] = {node: None for node in self.nodes}

        # Set inital values for start node
        g_scores[start] = 0
        f_scores[start] = self.heuristics[start]

        current_node: str = None
        while len(open_set) > 0:
            # Find the current node with the smallest f score
            current_node = None
            for node in open_set:
                if current_node is None or f_scores[node] < f_scores[current_node]:
                    current_node = node
            del node

            # If we have reached the target, reconstruct the path
            if current_node == target:
                break

            # Move the current node from the open set to the closed set
            open_set.remove(current_node)

            # Update g and f scores for neighbors
            for vertex in (v for v in self.vertices if v.start == current_node):
                neighbor = vertex.end
                tentative_g_score = g_scores[current_node] + vertex.cost
                if tentative_g_score < g_scores[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = vertex
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + self.heuristics[neighbor]
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        if current_node != target:
            return None
        del current_node

        # Reconstruct the path from start to target
        path = []
        current_vertex: Vertex = came_from[target]
        while current_vertex.start != start:
            path.append(current_vertex)
            current_vertex = came_from[current_vertex.start]

        path = list(reversed(path))
        return path
