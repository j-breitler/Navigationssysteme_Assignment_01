# Navigation Systems 2026/27 - Lab 1: Routing
# Dijkstra (time and distance) and A* (distance) for the street network of Graz

import math
import time
import heapq
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Files
# ----------------------------------------------------------------------
nodelist_file = "/home/julianb/Documents/Studium/LV/Navigationssysteme/Assignment_01/data/nodelist.txt"
nodepl_file = "/home/julianb/Documents/Studium/LV/Navigationssysteme/Assignment_01/data/nodepl.txt"
arclist_file = "/home/julianb/Documents/Studium/LV/Navigationssysteme/Assignment_01/data/arclist.txt"

# ----------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------

# our home
home = (47.08635507588021, 15.461469804462268)   # this is a tuple, because these coordinates are fixed and should not change

# our targets
targets = {"Basilika Mariatrost":9328, "Schloss Eggenberg":6031, "Murpark":8543} #dict

# colors for the targets in the plots
colors = {"Basilika Mariatrost":"blue", "Schloss Eggenberg":"red", "Murpark":"green"} #dict

# arcs above this are forbidden
oneway_limit = 1000

# earth radius in km
earth_radius = 6371.0




# ----------------------------------------------------------------------
# Load the coordinates
# ----------------------------------------------------------------------

# list for the coordinates, with a placeholder for index 0
"""
Since Python indexing starts at 0,
but the data starts at index 1
we create a placehodler for index 0.
"""
coordinates = [None]

# open the nodepl file
with open (nodepl_file) as nodepl:
    for line in nodepl:
        lat_lon = line.split()
        lat = float(lat_lon[0])
        lon = float(lat_lon[1])
        coordinates.append((lat,lon)) # append the coordiantes as a tuple (the coordinate pairs belong together and should not change)

number_of_nodes = len(coordinates) - 1

# ----------------------------------------------------------------------
# Load the nodelist
# ----------------------------------------------------------------------

# adjacency list of nodes
first_arc = [None]

# open the nodelist file
with open (nodelist_file) as nodelist:
    for line in nodelist:
        nodes = int(line)
        first_arc.append(nodes)

"""
The arcs of node i are in the rows first_arc[i] until first_arc[i+1] - 1.
The nodelist has one more entry than there are nodes,
so this also works for the last node.
"""

# ----------------------------------------------------------------------
# Load the arcs list
# ----------------------------------------------------------------------

# list for the arcs, with a placeholder for index 0
arcs = [None]

# open the arcslist file
with open (arclist_file) as arcs_list:
    for line in arcs_list:
        columns = line.split()
        destination = int(columns[0])
        travel_time = float(columns[1])     # hours
        length = float(columns[2])          # km
        speed_limit = float(columns[3])
        clazz = int(columns[4])
        flags = int(columns[5])
        arcs.append((destination, travel_time, length, speed_limit, clazz, flags)) # append the arc as a tuple (the values belong together and should not change)

# ----------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------

def haversine(point_1, point_2):
    """distance in km between two (lat, lon) tuples on the earth (Sphärischer Cosinussatz für Seiten)"""
    # unpack the tuples
    lat_1, lon_1 = point_1
    lat_2, lon_2 = point_2

    # degrees -> radians (sin and cos in Python need radians)
    lat_1 = lat_1 * math.pi / 180
    lon_1 = lon_1 * math.pi / 180

    lat_2 = lat_2 * math.pi / 180
    lon_2 = lon_2 * math.pi / 180

    # differences
    d_lat = lat_2 - lat_1
    d_lon = lon_2 - lon_1

    # haversine formula, split into small pieces
    sin_lat = math.sin(d_lat / 2)
    sin_lon = math.sin(d_lon / 2)
    a = sin_lat * sin_lat + math.cos(lat_1) * math.cos(lat_2) * sin_lon * sin_lon

    # central angle (in radians)
    c = 2 * math.asin(math.sqrt(a))

    # angle * earth radius = distance in km
    distance = earth_radius * c
    return distance



def outgoing_arcs(node):
    """all arcs that start at this node"""
    return arcs[first_arc[node]:first_arc[node + 1]]


def routing(start, goal, cost_type="time", a_star=False):
    """
    Dijkstra (a_star=False) or A* (a_star=True) from start to goal.
    cost_type: "time" -> column travel_time, "distance" -> column length
    Dijkstra: always continue with the open node with the smallest cost.
    
    A*: always continue with the open node with the smallest cost + heuristic.
        The heuristic is the straight-line distance to the goal. A road can
        never be shorter than the straight line, so A* still finds the
        optimal route (only valid for cost_type = "distance").
    """
    if cost_type == "time":
      cost_index = 1      # travel time [h]
    else:
      cost_index = 2      # length [km]

    cost = [math.inf] * (number_of_nodes + 1)       # best cost from start
    predecessor = [0] * (number_of_nodes + 1)       # where did we come from? (0 = none)
    done = [False] * (number_of_nodes + 1)          # is the cost final?
    visited = []                                    # for the plot: order of finished nodes

    cost[start] = 0
    open_nodes = [(0, start)]   # priority queue with (value, node)

    while open_nodes:
        value, current = heapq.heappop(open_nodes)

        # old entry in the queue -> node is already finished
        if done[current]:
            continue
        done[current] = True
        visited.append(current)

        # stop when we reached the goal
        if current == goal:
            break

        # look at all neighbours of the current node
        for arc in outgoing_arcs(current):
            neighbour = arc[0]

            # one-way street in the wrong direction -> skip
            if arc[1] > oneway_limit:
                continue

            if done[neighbour]:
                continue

            new_cost = cost[current] + arc[cost_index]

            # cheaper way found?
            if new_cost < cost[neighbour]:
                cost[neighbour] = new_cost
                predecessor[neighbour] = current
                if a_star:
                    value = new_cost + haversine(coordinates[neighbour], coordinates[goal])
                else:
                    value = new_cost
                heapq.heappush(open_nodes, (value, neighbour))

    return predecessor, cost[goal], visited


def get_path(predecessor, start, goal):
    """go backwards from the goal to the start"""
    path = [goal]
    node = goal
    while node != start:
        node = predecessor[node]
        path.append(node)
    path.reverse()
    return path


def path_time_and_distance(path):
    """add up time (h) and distance (km) of all arcs along the path"""
    total_time = 0
    total_distance = 0

    # go through the path in pairs: (node 0, node 1), (node 1, node 2), ...
    for i in range(len(path) - 1):
        node_from = path[i]
        node_to = path[i + 1]

        # find the arc from node_from to node_to
        for arc in outgoing_arcs(node_from):
            if arc[0] == node_to:
                total_time = total_time + arc[1]
                total_distance = total_distance + arc[2]
                break

    return total_time, total_distance


def save_prelist(filename, predecessor):
    """save the predecessor list: row number = node id, value = predecessor (0 = none)"""
    with open (filename, "w") as prelist:
        for node in range(1, number_of_nodes + 1):
            prelist.write(f'{predecessor[node]}\n')


def plot_streets():
    """draw all streets in grey (None starts a new line segment)"""
    x = []
    y = []
    for node in range(1, number_of_nodes + 1):
        for arc in outgoing_arcs(node):
            x += [coordinates[node][1], coordinates[arc[0]][1], None]
            y += [coordinates[node][0], coordinates[arc[0]][0], None]
    plt.plot(x, y, color="lightgrey", linewidth=0.4)


def plot_path(path, color, style, label):
    lats = []
    lons = []
    for node in path:
        lat, lon = coordinates[node]
        lats.append(lat)
        lons.append(lon)
    plt.plot(lons, lats, color=color, linestyle=style, linewidth=2, label=label)


def plot_search_tree(visited, predecessor, color):
    """draw the street from the predecessor to every visited node -> search area"""
    x = []
    y = []
    for node in visited:
        before = predecessor[node]
        if before != 0:
            x += [coordinates[before][1], coordinates[node][1], None]
            y += [coordinates[before][0], coordinates[node][0], None]
    plt.plot(x, y, color=color, linewidth=0.8, label="searched streets")


def finish_plot(title):
    plt.xlabel("Longitude [°]")
    plt.ylabel("Latitude [°]")
    plt.title(title)
    plt.gca().set_aspect(1 / math.cos(math.radians(home[0])))  # correct scale
    plt.grid(True)
    plt.legend(loc="upper left", fontsize=8)


  # ----------------------------------------------------------------------
  # Find the start node (node closest to home)
  # ----------------------------------------------------------------------

start = 0                     # best node found so far (0 = none yet)
start_distance = math.inf     # its distance to home (infinitely far at the beginning)

for node in range(1, number_of_nodes + 1):
    distance = haversine(home, coordinates[node])

    # closer than the best one so far? -> remember this node
    if distance < start_distance:
        start_distance = distance
        start = node

print(f'\nStart node: {start} ({start_distance * 1000:.0f} m from home)')


# ----------------------------------------------------------------------
# Task 1: Dijkstra with time and distance
# ----------------------------------------------------------------------

print('\nDijkstra')

plt.figure(figsize=(10, 9))
plot_streets()

for name, goal in targets.items():

    # Dijkstra, once optimised for time and once for distance
    pre_time, cost_time, visited_time = routing(start, goal, cost_type="time", a_star=False)
    pre_dist, cost_dist, visited_dist = routing(start, goal, cost_type="distance", a_star=False)

    # store the predecessor lists (prelist.txt from the lecture slides)
    save_prelist(f'prelist_time_{goal}.txt', pre_time)
    save_prelist(f'prelist_distance_{goal}.txt', pre_dist)

    path_time = get_path(pre_time, start, goal)
    path_dist = get_path(pre_dist, start, goal)

    time_t, dist_t = path_time_and_distance(path_time)
    time_d, dist_d = path_time_and_distance(path_dist)

    print(name)
    print(f'   cost = time:     {dist_t:.2f} km, {time_t * 60:.1f} min')
    print(f'   cost = distance: {dist_d:.2f} km, {time_d * 60:.1f} min')

    plot_path(path_time, colors[name], "-", f'opt. Route {name} (time)')
    plot_path(path_dist, colors[name], "--", f'opt. Route {name} (distance)')
    plt.plot(coordinates[goal][1], coordinates[goal][0], "ko")
    plt.text(coordinates[goal][1], coordinates[goal][0], f' {name}')

plt.plot(coordinates[start][1], coordinates[start][0], "k*", markersize=15, label="Start")
finish_plot("Dijkstra: time (solid) vs. distance (dashed)")
plt.savefig("dijkstra_time_distance.png", dpi=200)
plt.close()


# ----------------------------------------------------------------------
# Task 2.2: Dijkstra vs. A* (cost = distance)
# ----------------------------------------------------------------------

print('\nDijkstra vs. A*')

for name, goal in targets.items():

    # Dijkstra
    t0 = time.perf_counter()
    pre_dij, cost_dij, visited_dij = routing(start, goal, cost_type="distance", a_star=False)
    t1 = time.perf_counter()

    # A*
    pre_ast, cost_ast, visited_ast = routing(start, goal, cost_type="distance", a_star=True)
    t2 = time.perf_counter()

    path_dij = get_path(pre_dij, start, goal)
    path_ast = get_path(pre_ast, start, goal)

    print(name)
    print(f'   Dijkstra: {cost_dij:.3f} km, visited nodes: {len(visited_dij)}, runtime: {(t1 - t0) * 1000:.1f} ms')
    print(f'   A*:       {cost_ast:.3f} km, visited nodes: {len(visited_ast)}, runtime: {(t2 - t1) * 1000:.1f} ms')

    plt.figure(figsize=(16, 8))

    # left: Dijkstra, right: A*
    results = [("Dijkstra", path_dij, cost_dij, visited_dij, pre_dij),
               ("A*", path_ast, cost_ast, visited_ast, pre_ast)]

    for i, (algorithm, path, cost, visited, predecessor) in enumerate(results):
        plt.subplot(1, 2, i + 1)
        plot_streets()
        plot_search_tree(visited, predecessor, "lightskyblue")
        plot_path(path, "red", "-", f'opt. Route ({cost:.2f} km)')
        plt.plot(coordinates[start][1], coordinates[start][0], "k*", markersize=15, label="Start")
        plt.plot(coordinates[goal][1], coordinates[goal][0], "ko", label=name)
        finish_plot(f'{algorithm} - {len(visited)} visited nodes')

    plt.tight_layout()
    plt.savefig(f'dijkstra_vs_astar_{goal}.png', dpi=200)
    plt.close()

print('\nDone! The plots are saved as .png files.')
