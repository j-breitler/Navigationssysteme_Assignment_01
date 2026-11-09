# The Program, Step by Step

This file describes `Assigment_01_BREITLER_STERING.py` **as it is written**, from top to bottom.

Each step tells you:
- **What** happens (with line numbers)
- **Which variable** the result goes into and **where** it is used later
- **Which functions** are used: our own functions and the ones from Python and its libraries. For each one: what it does, and why we need it at that point

At the end there is a **function reference** (appendix). It lists every function in one place.

---

## Overview: the order of the program

```
Step 0  Imports, file paths, settings                     (lines 4–33)
Step 1  Load coordinates      nodepl.txt   → coordinates  (lines 42–58)
Step 2  Load pointers         nodelist.txt → first_arc    (lines 64–77)
Step 3  Load arcs             arclist.txt  → arcs         (lines 83–96)
Step 4  Helper functions      haversine, outgoing_arcs    (lines 102–135)
Step 5  Routing               routing() = Dijkstra / A*   (lines 138–198)
Step 6  Rebuild the path      get_path()                  (lines 201–209)
Step 7  Time and length       path_time_and_distance()    (lines 212–229)
Step 8  Save predecessors     save_prelist()              (lines 232–236)
Step 9  Plot helpers          plot_streets, plot_path,
                              plot_search_tree, finish_plot (lines 239–278)
Step 10 Find the start node   → start                     (lines 285–296)
Step 11 Task 1: Dijkstra, time vs. distance               (lines 303–336)
Step 12 Task 2.2: Dijkstra vs. A*                         (lines 343–382)
```

Steps 4–9 only **define** functions. Nothing is calculated when Python reads them. The real work starts in step 10, and steps 11 and 12 call these functions.

## Overview of the important variables

| Variable | Data type | Contents | Created in | Used in |
|---|---|---|---|---|
| `home` | tuple `(lat, lon)` | our home coordinates | step 0 | 9 (`finish_plot`), 10 |
| `targets` | dict `{str: int}` | name → node ID of the 3 targets | step 0 | 11, 12 |
| `colors` | dict `{str: str}` | name → plot colour | step 0 | 11 |
| `oneway_limit` | int | arcs with a larger time are forbidden | step 0 | 5 |
| `earth_radius` | float | 6371 km | step 0 | 4 (`haversine`) |
| `coordinates` | list of tuples `(lat, lon)` | coordinates per node, `None` at index 0 | step 1 | 4, 5, 9, 10 |
| `number_of_nodes` | int | 9504 | step 1 | 5, 8, 9, 10 |
| `first_arc` | list of int | start row in `arcs` for each node | step 2 | 4 (`outgoing_arcs`) |
| `arcs` | list of tuples | every arc as `(dest, time, length, speed, clazz, flags)` | step 3 | 4 (`outgoing_arcs`) |
| `start`, `start_distance` | int, float | the node closest to `home` and its distance [km] | step 10 | 11, 12 |
| `predecessor`, `cost`, `visited` | lists | results of one routing run | step 5 | 6, 7, 8, 9 |

## Overview of our own functions

| Function | Input → output | Called by / in |
|---|---|---|
| `haversine(point_1, point_2)` | two `(lat, lon)` → distance in km | `routing` (A* heuristic), step 10 (start node) |
| `outgoing_arcs(node)` | node ID → list of its arcs | `routing`, `path_time_and_distance`, `plot_streets` |
| `routing(start, goal, cost_type, a_star)` | → `predecessor`, cost to goal, `visited` | step 11, step 12 |
| `get_path(predecessor, start, goal)` | → list of nodes from start to goal | step 11, step 12 |
| `path_time_and_distance(path)` | → total time [h], total length [km] | step 11 |
| `save_prelist(filename, predecessor)` | → writes a text file | step 11 |
| `plot_streets()` | → draws the whole street network in grey | step 11, step 12 |
| `plot_path(path, color, style, label)` | → draws one route | step 11, step 12 |
| `plot_search_tree(visited, predecessor, color)` | → draws the searched streets | step 12 |
| `finish_plot(title)` | → axis labels, title, aspect ratio, grid, legend | step 11, step 12 |

---

## Step 0 – Imports and settings (lines 4–33)

**Imports (lines 4–7):**

| Import | Why we need it |
|---|---|
| `import math` | `math.pi`, `math.sin`, `math.cos`, `math.asin`, `math.sqrt` for haversine. `math.radians` and `math.cos` for the aspect ratio of the plots. `math.inf` as the start value "not reached yet" / "infinitely far away" |
| `import time` | `time.perf_counter()` to measure the runtime of Dijkstra and A* (step 12) |
| `import heapq` | The priority queue in `routing()`: it always gives back the open node with the smallest value |
| `import matplotlib.pyplot as plt` | All plots. `as plt` is only a shorter name |

`import` loads a module once at the top. After that, its functions can be used anywhere in the file as `module.function(...)`.

**File paths (lines 12–14):** `nodelist_file`, `nodepl_file`, `arclist_file`. All three paths are written in one place, so if the folder changes you only edit these lines.
> ⚠️ At the moment they are **absolute** paths that point to `../Assignment_01/data/`. For the ZIP submission they should be relative: `"data/nodepl.txt"` and so on.

**Settings (lines 21–33):**
- `home = (47.086…, 15.461…)` – a **tuple**, because latitude and longitude belong together and must not change.
- `targets = {"Basilika Mariatrost": 9328, "Schloss Eggenberg": 6031, "Murpark": 8543}` – a **dict**, because we look things up by name. The names also become the labels in the plots.
- `colors = {...}` – also a dict with the same keys, so `colors[name]` gives the colour of a target.
- `oneway_limit = 1000` – one-way streets in the wrong direction have time = 1,000,000 h in the data. Anything above 1000 counts as forbidden.
- `earth_radius = 6371.0` – mean Earth radius in km, used in `haversine`.

## Step 1 – Load the coordinates (lines 42–58)

**The placeholder idea (comment, lines 43–47):** the data starts counting at 1, but Python lists start at 0. So every list gets a `None` at index 0. After that, `coordinates[5]` really is node 5 and no `+1`/`-1` is ever needed.

```python
coordinates = [None]
with open(nodepl_file) as nodepl:
    for line in nodepl:
        lat_lon = line.split()
        lat = float(lat_lon[0])
        lon = float(lat_lon[1])
        coordinates.append((lat, lon))
number_of_nodes = len(coordinates) - 1
```

Functions used:
- **`open(path)`** – opens the file for reading. Used together with **`with`**, so the file is closed again automatically at the end of the block, even if an error happens.
- **`for line in nodepl`** – a file can be looped over directly. Each loop pass gives one line as a string, e.g. `"  47.0527089  15.4404670\n"`.
- **`str.split()`** – without an argument, it splits at any amount of whitespace and also removes the `\n`. Result: `["47.0527089", "15.4404670"]`.
- **`float(...)`** – turns the text into a decimal number. We need this because you can't calculate with text.
- **`list.append(x)`** – adds `x` at the end of the list. Because node 1 is in line 1, it lands at index 1 (index 0 is the placeholder).
- **`len(list)`** – number of elements. `- 1` removes the placeholder → `number_of_nodes = 9504`.

Result: `coordinates[node] = (lat, lon)`. It is used for the distance to `home` (step 10), the A* heuristic (step 5) and every plot (step 9).

## Step 2 – Load the pointers (`first_arc`, lines 64–77)

```python
first_arc = [None]
with open(nodelist_file) as nodelist:
    for line in nodelist:
        nodes = int(line)
        first_arc.append(nodes)
```

- **`int(line)`** – turns the text into a whole number. `int()` ignores the spaces and the `\n` around the number.
- `first_arc[i]` = the row in `arcs` where the arcs of node `i` start.

**Why it works for the last node (comment, lines 73–77):** `nodelist.txt` has **9505** values, one more than there are nodes. (`wc -l` shows 9504 only because the last line has no newline.) The last value, 22341, is "one past the end" of `arcs`. So the rule "the arcs of node `i` are in rows `first_arc[i]` to `first_arc[i+1] − 1`" also works for node 9504, without a special case.

## Step 3 – Load the arcs (lines 83–96)

```python
arcs = [None]
with open(arclist_file) as arcs_list:
    for line in arcs_list:
        columns = line.split()
        ...
        arcs.append((destination, travel_time, length, speed_limit, clazz, flags))
```

- `split()` gives 6 strings. The IDs (`destination`, `clazz`, `flags`) are turned into numbers with **`int()`**, and the measurements (`travel_time` [h], `length` [km], `speed_limit` [km/h]) with **`float()`**.
- Each arc is stored as **one tuple**. An arc is a fixed record that never changes.
- The positions in the tuple matter later: `arc[0]` = destination, `arc[1]` = time, `arc[2]` = length. (Positions 3–5 are loaded but not used for routing.)
- The **start** node is not stored in the arc. It follows from which node's row range the arc is in (see `outgoing_arcs`).

## Step 4 – Helper functions (lines 102–135)

### `haversine(point_1, point_2)` → distance in km (lines 102–129)

```python
# unpack the tuples
lat_1, lon_1 = point_1
lat_2, lon_2 = point_2

# degrees -> radians
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
```

**What it does:** computes the great-circle distance (the straight line along the Earth's surface) between two coordinates.

**Where and why it is needed:**
1. **Step 10:** to find the node closest to `home`, in real km instead of degrees. (One degree of longitude is shorter than one degree of latitude in Graz, and haversine handles that automatically.)
2. **Step 5, A\*:** as the **heuristic**, the estimated remaining distance to the goal. A road can't be shorter than the straight line, so the estimate never overestimates the real distance.

The function, line by line:
1. **Unpack the tuples:** `lat_1, lon_1 = point_1` puts the two values of the tuple into two variables.
2. **Degrees → radians:** `* math.pi / 180`. `math.sin` and `math.cos` expect radians, but our data is in degrees. **`math.pi`** is π = 3.14159…
3. **Differences** Δφ and Δλ.
4. **The formula for `a`:** `sin_lat * sin_lat` is sin² (squared). The two sine values are stored first, so the line for `a` stays short. **`math.sin`, `math.cos`** = sine, cosine.
5. **Central angle `c`:** **`math.sqrt`** = square root, **`math.asin`** = arcsine (inverse sine). The result is the angle between the two points, seen from the centre of the Earth, in radians.
6. **Distance:** angle (radians) × radius = arc length in km. This only works because the angle is in radians, so there's no need to convert back to degrees.

**German terms from the GeoMathe 1 script (`Skriptum.pdf`):**

The name "haversine" doesn't appear in the script, but the formula does. Page numbers below are the printed ones (PDF page = printed page + 1).

| In the code | German term in the script | Where in the script |
|---|---|---|
| `lat`, `lon` (φ, λ) | **geographische Breite** φ, **geographische Länge** λ | II.2 Sphärische Geometrie, p. 49 |
| degrees in the data | **Altgrad** (0° … 360°) | I.1 Winkelmaße, p. 3 |
| `* math.pi / 180` | Umrechnung **Altgrad → Bogenmaß**: α̂ = α° / ρ° with ρ° = 180°/π | I.1 Winkelmaße, p. 3 |
| `math.sin`, `math.cos` | **Trigonometrische Funktionen**: Sinus, Kosinus | I.2, p. 4 |
| the triangle north pole – P1 – P2 | **Poldreieck** (a **sphärisches Dreieck** whose sides are **Großkreisbögen**) | II.1 p. 40, II.2 p. 50 |
| sides 90° − φ1, 90° − φ2 | sin(90° − φ) = cos φ: **Komplementärwinkel** | I.2, p. 5 |
| `d_lon` = Δλ | the angle α at the pole in the Poldreieck | II.2, p. 50 |
| the whole formula for `a` | **Sphärischer Cosinussatz für Seiten**, **numerisch stabile Alternative**: sin(a/2) = √( sin²((b−c)/2) + sin b · sin c · sin²(α/2) ) | II.1, p. 44 |
| `math.asin(math.sqrt(a))` | solving for a/2: **Arkussinus** of the **Quadratwurzel** | II.1, p. 44 (formula solved for a) |
| `c` = the central angle in radians | **sphärische Distanz** s12 (as an angle, in Bogenmaß) | II.2, p. 51 |
| `earth_radius * c` | arc length = R · α̂ (**Bogenmaß** = arc length on the **Einheitskreis**) | I.1, p. 3 |
| the task "distance between two known points" | **Zweite Grundaufgabe (2. HA)**: given P1, P2 → wanted s12 (and the azimuths α12, α21) | II.2, p. 51 |

How the script's formula becomes ours: in the Poldreieck, b = 90° − φ1, c = 90° − φ2, α = Δλ, and a = the distance we're looking for. Then (b − c)/2 = Δφ/2, sin b = cos φ1 and sin c = cos φ2, which gives exactly the line for `a` in the code.

**Why the "numerisch stabile Alternative" and not the normal Seitencosinussatz?** In the script, the 2. HA is solved with the normal **Seitencosinussatz**: cos s = sin φ1 sin φ2 + cos φ1 cos φ2 cos Δλ. For short distances (a few km in Graz), cos s is almost exactly 1, and taking the **Arkuskosinus** of a value that close to 1 loses a lot of precision. The sin² form avoids this, which is why the code uses it.

### `outgoing_arcs(node)` → list of arcs (lines 133–135)

```python
return arcs[first_arc[node]:first_arc[node + 1]]
```

**What it does:** returns all arcs that start at `node`.
**Where it is needed:** wherever we have to look at the neighbours of a node: in `routing` (expanding a node), `path_time_and_distance` (finding the arc between two path nodes) and `plot_streets` (drawing all streets).

- **Slicing `list[a:b]`** – gives the elements from index `a` up to **but not including** `b`. This matches the rule "rows `first_arc[i]` to `first_arc[i+1] − 1`" exactly.
- Example: node 1 → `arcs[1:5]` → rows 1, 2, 3, 4 → 4 arcs to nodes 2, 491, 7388, 2323.
- We don't build a separate `graph` list of lists. Slicing on demand is enough and saves memory.

## Step 5 – `routing(start, goal, cost_type="time", a_star=False)` (lines 138–198)

**One function for both algorithms:**
- `a_star=False` → **Dijkstra**: always continue with the open node that has the smallest cost so far.
- `a_star=True` → **A\***: always continue with the open node that has the smallest *cost so far + estimated rest* (haversine to the goal). Only valid with `cost_type="distance"`, because the heuristic is in km.

`cost_type="time"` and `a_star=False` are **default values**: if the caller leaves them out, these values are used. In steps 11 and 12 we still write them out, so every call shows what it does.

**Choosing the cost column (lines 149–152):**
```python
if cost_type == "time":
    cost_index = 1      # travel time [h]
else:
    cost_index = 2      # length [km]
```
An arc is `(destination, travel_time, length, ...)`, so index 1 is the time and index 2 is the length. Later, `arc[cost_index]` reads the right column. That way the same code works for both costs. The decision is made once per routing run, not for every arc.

**Preparation (lines 154–160):**

| Variable | Initial value | Data type and why |
|---|---|---|
| `cost` | `[math.inf] * (number_of_nodes + 1)` | **List**, one value per node (index = node ID). **`math.inf`** (infinity) means "not reached yet", and any real cost is smaller than it. `[x] * n` builds a list with `n` copies of `x`. |
| `predecessor` | `[0] * (number_of_nodes + 1)` | **List**, for each node the node we came from. `0` = none (there is no node 0). This list **is** the predecessor list from the slides. |
| `done` | `[False] * (number_of_nodes + 1)` | **List of booleans**: is the cost of this node final? `done[node]` is answered instantly, just like a set would be. |
| `visited` | `[]` | **List** of finished nodes **in the order** they were finished. Used for the plot and for counting (`len(visited)`) in step 12. A list keeps the order, a set wouldn't. |
| `open_nodes` | `[(0, start)]` | **List used as a heap**. Entries are tuples `(value, node)`. `heapq` compares tuples by their **first** element, so the value has to come first. |

`cost[start] = 0` – the start costs nothing.

**The main loop (lines 162–196):**

1. `while open_nodes:` – an empty list counts as `False`, so the loop runs as long as there are open nodes.
2. **`heapq.heappop(open_nodes)`** – removes and returns the entry with the **smallest** value. `value, current = ...` unpacks the tuple. (`value` itself isn't needed after this, because the real cost is in `cost[current]`.)
3. `if done[current]: continue` – **lazy deletion**: when a node gets a better cost, we just push it again and leave the old entry in the heap. When the old entry comes out later, the node is already done, and we skip it. **`continue`** jumps to the next loop pass.
4. `done[current] = True` and `visited.append(current)` – from now on, `cost[current]` is final.
5. `if current == goal: break` – **stop early** as soon as the goal is finished. **`break`** leaves the loop. Both algorithms stop here, so the comparison in step 12 is fair.
6. `for arc in outgoing_arcs(current):` – look at all neighbours.
   - `neighbour = arc[0]`
   - `if arc[1] > oneway_limit: continue` – **one-way street in the wrong direction**. The check is always on the **time** column (`arc[1]`), because the length of these arcs is normal. Without this line, a distance route would drive the wrong way down one-way streets.
   - `if done[neighbour]: continue` – a finished node can't get any better.
   - `new_cost = cost[current] + arc[cost_index]`
   - `if new_cost < cost[neighbour]:` → better way found:
     - `cost[neighbour] = new_cost`
     - `predecessor[neighbour] = current`
     - Priority value: Dijkstra → `new_cost`. A\* → `new_cost + haversine(coordinates[neighbour], coordinates[goal])`.
     - **`heapq.heappush(open_nodes, (value, neighbour))`** – adds the entry and keeps the heap order.
7. `return predecessor, cost[goal], visited` (line 198) – returns three values at once, as a tuple. The caller unpacks them: `pre, cost, visited = routing(...)`.

**Why `heapq` and not a plain list?** A plain list works too: search the open node with the smallest cost with a `for` loop, then remove it with `list.remove`. We tested it: the routes are identical, but it is 3–5 times slower (e.g. Murpark 22 ms instead of 4.5 ms), because it has to look at **every** open node in each loop pass. `heapq` keeps the list in a special order (a "heap"), where the smallest element is always at position 0. Taking it out or adding a new element only costs a few comparisons.

> **Note:** because of the early stop, `predecessor` is only complete for the finished nodes. That's enough for the route to `goal`, but it is not a full shortest-path tree of the whole city.

## Step 6 – `get_path(predecessor, start, goal)` (lines 201–209)

```python
path = [goal]
node = goal
while node != start:
    node = predecessor[node]
    path.append(node)
path.reverse()
return path
```

**What it does:** walks backwards through the predecessor list, from the goal to the start, and collects the nodes.
**Why needed:** `routing` only returns predecessors, but for plotting and for summing time and length we need the actual sequence of nodes.

- **`list.reverse()`** – reverses the list **in place** (it changes the list itself and returns nothing). We need it because we collected the nodes from goal to start.
- A **list** fits here because a path has an order and grows step by step.
> ⚠️ There is no protection against an unreachable goal. Then `predecessor[goal]` would be 0, and since `predecessor[0]` is also 0, the loop would never end. With our three targets this doesn't happen.

## Step 7 – `path_time_and_distance(path)` (lines 212–229)

**What it does:** adds up travel time [h] and length [km] of all arcs along a path.
**Why needed:** a route that is optimal for *time* still has a length, and the other way round. Comparing both values for both routes is the core of task 1.

```python
for i in range(len(path) - 1):
    node_from = path[i]
    node_to = path[i + 1]

    for arc in outgoing_arcs(node_from):
        if arc[0] == node_to:
            total_time = total_time + arc[1]
            total_distance = total_distance + arc[2]
            break
```

- **Go through the path in pairs:** `path[i]` and `path[i + 1]` are two neighbouring nodes of the route, so together they are exactly one arc.
- **`range(len(path) - 1)`** – the positions 0 … (number of nodes − 2). The `- 1` is needed because the last node has no next node; `path[i + 1]` would not exist.
- Inside, `outgoing_arcs(node_from)` is searched for the arc that leads to `node_to`. **`break`** stops the search once it's found.
- Returns `total_time, total_distance` (hours, km). The conversion to minutes (`* 60`) happens later in the print.

## Step 8 – `save_prelist(filename, predecessor)` (lines 232–236)

**What it does:** writes the predecessor list to a text file. Line number = node ID, value = predecessor (0 = none), in the same format as the given data files.
**Why needed:** the lecture slides ask for the predecessor list to be stored (`prelist.txt`).

- **`open(filename, "w")`** – `"w"` = write mode. It creates the file, or overwrites it if it already exists.
- **`range(1, number_of_nodes + 1)`** – the numbers 1 … 9504. The end value is **not** included, hence `+ 1`. We start at 1 to skip the placeholder.
- **`file.write(text)`** – writes text. Unlike `print`, it doesn't add a newline by itself, so `\n` is added in the f-string.

## Step 9 – Plot helper functions (lines 239–278)

### `plot_streets()` – the grey background network (lines 239–247)

```python
for node in range(1, number_of_nodes + 1):
    for arc in outgoing_arcs(node):
        x += [coordinates[node][1], coordinates[arc[0]][1], None]
        y += [coordinates[node][0], coordinates[arc[0]][0], None]
plt.plot(x, y, color="lightgrey", linewidth=0.4)
```

- **x = longitude (`[1]`), y = latitude (`[0]`)**: east–west goes on the horizontal axis.
- **The `None` trick:** `plt.plot` draws one connected line through all points, but a `None` value interrupts it. So `[start, end, None]` gives a separate line piece per arc, and **one** `plt.plot` call draws all 22,340 arcs. That is much faster than 22,340 separate calls.
- `list += [...]` appends several elements at once.
- **`plt.plot(x, y, color=..., linewidth=...)`** – draws lines through the points.

### `plot_path(path, color, style, label)` – one route (lines 250–257)

```python
lats = []
lons = []
for node in path:
    lat, lon = coordinates[node]
    lats.append(lat)
    lons.append(lon)
plt.plot(lons, lats, color=color, linestyle=style, linewidth=2, label=label)
```

- `plt.plot` needs **two separate lists**: all x values (longitudes) and all y values (latitudes). The loop builds them one node at a time; tuple unpacking `lat, lon = coordinates[node]` splits each coordinate pair.
- `linestyle="-"` = solid, `"--"` = dashed. `label` is the text shown in the legend.

### `plot_search_tree(visited, predecessor, color)` – the searched area (lines 260–269)

For every visited node, it draws the street from its predecessor to it (skipped if the predecessor is 0, i.e. for the start). It uses the same `None` trick as `plot_streets`.
**Why needed:** this shows *how much* of the network each algorithm searched. Dijkstra spreads out in a circle, while A\* heads towards the goal. This is the main picture for the comparison in step 12.

### `finish_plot(title)` – common formatting (lines 272–278)

- **`plt.xlabel` / `plt.ylabel`** – axis labels with units (required by the assignment).
- **`plt.title`** – the title above the plot.
- **`plt.gca()`** – "get current axes": the plot area currently being drawn in. Needed to call `.set_aspect(...)` on it.
- **`.set_aspect(1 / math.cos(math.radians(home[0])))`** – the aspect ratio. At our latitude, 1° of longitude is only cos(47°) ≈ 0.68 times as long as 1° of latitude. Without this correction, Graz would look stretched from east to west. `home[0]` is our latitude, which is close enough for the whole city. **`math.radians`** converts degrees → radians, the same as `* math.pi / 180` in `haversine`. (Script: Umrechnung **Altgrad → Bogenmaß**, I.1; **Kosinus**, I.2.)
- **`plt.grid(True)`** – shows a grid.
- **`plt.legend(loc="upper left", fontsize=8)`** – the legend, built from all `label=...` values.

All plot helpers are written once and then used in both task 1 and task 2.2.

## Step 10 – Find the start node (lines 285–296)

```python
start = 0                     # best node found so far (0 = none yet)
start_distance = math.inf     # its distance to home (infinitely far at the beginning)

for node in range(1, number_of_nodes + 1):
    distance = haversine(home, coordinates[node])

    # closer than the best one so far? -> remember this node
    if distance < start_distance:
        start_distance = distance
        start = node
```

**What it does:** finds the node that is closest to `home`. It becomes the start of every route.

1. Before the loop there's no best node yet: `start = 0` and `start_distance = math.inf`. Any real distance is smaller than infinity, so the first node always becomes the first "best" node.
2. The loop checks every node from 1 to 9504 (index 0 is the placeholder).
3. If a node is closer than the best one so far, we store both the node **and** its distance.
4. After the loop, `start` is the closest node and `start_distance` its distance in km.

- **Why two plain variables instead of a list of all distances?** We only need the minimum. Storing 9504 values just to search through them again would be pointless.
- The print uses `start_distance * 1000` → metres, and `{...:.0f}` = 0 decimal places. Result: **node 6386, 75 m from home**.

## Step 11 – Task 1: Dijkstra with time and distance (lines 303–336)

1. **`plt.figure(figsize=(10, 9))`** – a new, empty figure that is 10 × 9 inches. `plot_streets()` draws the background.
2. **`for name, goal in targets.items():`** – we have 3 targets, and for each one we do exactly the same steps. The loop means we write those steps **once**. **`dict.items()`** gives the pairs `("Basilika Mariatrost", 9328)` and so on, so we get the name (for prints and labels) and the node ID (for routing) at the same time.
3. For each target:
   - **Routing (lines 311–312):**
     ```python
     pre_time, cost_time, visited_time = routing(start, goal, cost_type="time", a_star=False)
     pre_dist, cost_dist, visited_dist = routing(start, goal, cost_type="distance", a_star=False)
     ```
     **Named arguments** (`cost_type=...`, `a_star=...`): the call says exactly what it does, which cost and which algorithm. For Python the result is the same as without the names.
   - `save_prelist(...)` → `results/prelists/prelist_time_<goal>.txt` and `results/prelists/prelist_distance_<goal>.txt` (6 files in total). The paths are relative, so the script has to be started from the project folder.
   - `get_path(...)` → both routes as node lists.
   - `path_time_and_distance(...)` → time **and** length of both routes, so each route can be judged by both measures.
   - `print` with **format specs**: `{dist_t:.2f}` = 2 decimal places, `{time_t * 60:.1f}` = hours → minutes with 1 decimal place.
   - `plot_path(...)` → time route solid (`"-"`), distance route dashed (`"--"`), in the target's colour `colors[name]`.
   - `plt.plot(lon, lat, "ko")` – the **format string** `"ko"`: `k` = black, `o` = circle marker. It marks the target.
   - **`plt.text(x, y, text)`** – writes the target name next to the marker.
4. After the loop: start marker `"k*"` (black star, `markersize=15`), then `finish_plot(...)`.
5. **`plt.savefig("results/dijkstra_time_distance.png", dpi=200)`** – saves the figure. `dpi` = resolution.
6. **`plt.close()`** – closes the figure and frees its memory, so the next plot starts empty.

Results:

| Target | time-optimal | distance-optimal |
|---|---|---|
| Basilika Mariatrost | 3.67 km, 4.7 min | 3.67 km, 4.7 min (same route) |
| Schloss Eggenberg | 7.45 km, 9.4 min | 7.12 km, 10.6 min |
| Murpark | 6.63 km, 8.4 min | 6.17 km, 9.5 min |

## Step 12 – Task 2.2: Dijkstra vs. A\* (lines 343–382)

Again one loop pass per target (`for name, goal in targets.items():`).

1. **Routing with runtime measurement (lines 347–354):**
   ```python
   # Dijkstra
   t0 = time.perf_counter()
   pre_dij, cost_dij, visited_dij = routing(start, goal, cost_type="distance", a_star=False)
   t1 = time.perf_counter()

   # A*
   pre_ast, cost_ast, visited_ast = routing(start, goal, cost_type="distance", a_star=True)
   t2 = time.perf_counter()
   ```
   - Both runs use `cost_type="distance"`, because the haversine heuristic is a distance. The only difference between the two calls is `a_star=False` / `a_star=True`.
   - **`time.perf_counter()`** returns a very precise clock value in seconds. Only the **difference** between two calls has a meaning: `t1 - t0` = Dijkstra, `t2 - t1` = A\*. `* 1000` → milliseconds. (One measurement per run, so the values vary a bit from run to run.)
2. `get_path(...)` for both results.
3. `print` shows the route cost (3 decimal places), **`len(visited)`** = number of visited nodes, and the runtime.
4. **Plot with two panels side by side (lines 363–380):**
   - `plt.figure(figsize=(16, 8))` – a wide figure.
   - `results = [("Dijkstra", ...), ("A*", ...)]` – a list with one tuple per algorithm, so that **one** loop can draw both panels.
   - **`enumerate(results)`** – gives the position `i` (0, 1) together with the element. `i` is needed to choose the panel.
   - The tuple is unpacked directly in the loop header: `for i, (algorithm, path, cost, visited, predecessor) in ...`.
   - **`plt.subplot(1, 2, i + 1)`** – 1 row, 2 columns, panel number `i + 1` (subplot numbers start at 1).
   - In each panel: `plot_streets()` → `plot_search_tree(...)` in light blue → `plot_path(...)` in red → start and goal markers → `finish_plot(...)` with the number of visited nodes in the title.
   - **`plt.tight_layout()`** – adjusts the spacing so that the two panels and their labels don't overlap.
   - `plt.savefig(f'results/dijkstra_vs_astar_{goal}.png', dpi=200)` and `plt.close()`.

Results:

| Target | Route length | Visited nodes Dijkstra / A\* |
|---|---|---|
| Basilika Mariatrost | 3.666 km (both) | 1829 / 122 |
| Schloss Eggenberg | 7.115 km (both) | 6135 / 1354 |
| Murpark | 6.167 km (both) | 4964 / 899 |

Both algorithms find the same route length, so the heuristic works. A\* only visits about 7–22 % of the nodes that Dijkstra visits.

---

## Appendix – Function reference

### Our own functions
See the table at the top: "Overview of our own functions".

### Python built-ins

| Function | What it does | Where used |
|---|---|---|
| `open(path)` / `open(path, "w")` | open a file for reading / writing | steps 1–3, 8 |
| `with ... as ...` | closes the file automatically afterwards | steps 1–3, 8 |
| `str.split()` | splits a line at whitespace into a list of strings | steps 1, 3 |
| `float(x)` / `int(x)` | text → decimal number / whole number | steps 1–3 |
| `len(x)` | number of elements | steps 1, 7, 12 |
| `print(...)` | output to the terminal | steps 10–12 |
| `range(a, b)` / `range(n)` | numbers `a` … `b−1` / `0` … `n−1` | steps 7, 8, 9, 10 |
| `enumerate(list)` | position + element | step 12 |
| `dict.items()` | (key, value) pairs | steps 11, 12 |
| `list.append(x)` | adds one element at the end | steps 1–3, 5, 6, 9 |
| `list += [...]` | adds several elements at the end | step 9 |
| `list.reverse()` | reverses the list in place | `get_path` |
| `file.write(text)` | writes text to a file | `save_prelist` |
| `list[a:b]` (slicing) | part of a list, `b` not included | `outgoing_arcs` |
| tuple unpacking `a, b = t` | puts the values of a tuple into separate variables | `haversine`, `plot_path`, `routing`, steps 11, 12 |
| f-string `f'{x:.2f}'` | inserts values into text, with formatting | all prints, file names |

### `math`

| Function | What it does | German term (GeoMathe 1 script) | Where used |
|---|---|---|---|
| `math.pi` | π = 3.14159… | π (in ρ° = 180°/π, I.1) | `haversine` (degrees → radians) |
| `math.radians` | degrees → radians | Umrechnung Altgrad → Bogenmaß (I.1) | `finish_plot` |
| `math.sin`, `math.cos` | sine, cosine | Sinus, Kosinus – trigonometrische Funktionen (I.2) | `haversine`, `finish_plot` (cos) |
| `math.asin` | arcsine | Arkussinus | `haversine` |
| `math.sqrt` | square root | Quadratwurzel | `haversine` |
| `math.inf` | infinity ("not reached yet" / "infinitely far") | – | `routing`, step 10 |

### `heapq`

| Function | What it does | Where used |
|---|---|---|
| `heapq.heappush(heap, item)` | adds an item, keeps the smallest one at the front | `routing` |
| `heapq.heappop(heap)` | removes and returns the smallest item | `routing` |

### `time`

| Function | What it does | Where used |
|---|---|---|
| `time.perf_counter()` | precise clock for measuring time differences | step 12 |

### `matplotlib.pyplot` (as `plt`)

| Function | What it does | Where used |
|---|---|---|
| `plt.figure(figsize=...)` | new, empty figure | steps 11, 12 |
| `plt.subplot(rows, cols, n)` | chooses panel `n` in a grid | step 12 |
| `plt.plot(x, y, ...)` | lines or markers (format strings `"ko"`, `"k*"`) | plot helpers, steps 11, 12 |
| `plt.text(x, y, s)` | text in the plot | step 11 |
| `plt.xlabel`, `plt.ylabel`, `plt.title` | labels | `finish_plot` |
| `plt.gca().set_aspect(r)` | aspect ratio of the current axes | `finish_plot` |
| `plt.grid(True)` | grid | `finish_plot` |
| `plt.legend(...)` | legend from the `label=` values | `finish_plot` |
| `plt.tight_layout()` | fixes overlapping panels | step 12 |
| `plt.savefig(name, dpi=...)` | saves the figure as an image | steps 11, 12 |
| `plt.close()` | closes the figure, frees memory | steps 11, 12 |
