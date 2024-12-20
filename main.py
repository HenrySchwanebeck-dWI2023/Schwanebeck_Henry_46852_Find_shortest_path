import read_csv
import graph
import sys

usage = "Usage: 'python3 ./main.py <csvfile> <start> <target> <algorithm>'\nAlgorithm can be one of: [greedy, djikstra, astar]."

# check number of arguments
if len(sys.argv) != 5:
    print("Incorrect amount of args.\n" + usage)
    exit(1)

# save arguments in variables
csvfile = sys.argv[1]
start = sys.argv[2]
target = sys.argv[3]
algorithm = sys.argv[4].lower()

# check if algorithm is valid
if algorithm not in ["greedy", "djikstra", "astar"]:
    print("Incorrect algorithm.\n" + usage)
    exit(1)

# read content of csv file
csv_content: list[list[str]] = read_csv.read_file(csvfile)
g = graph.Graph(csv_content)

# check if start and target are valid nodes
if start not in g.nodes or target not in g.nodes:
    print("Start or end not a node of given Graph.\n" + usage)

# calculate path
path: list[graph.Vertex] = None
match algorithm:
    case "greedy":
        path = g.greedy(start=start, target=target)
    case "djikstra":
        path = g.djikstra(start=start, target=target)
    case "astar":
        path = g.a_star(start=start, target=target)

# calculate costs
cost = sum(v.cost for v in path)

# print calculated costs and path
print("{}: Cost: {}; Path:{}".format(algorithm, cost, path))
