# The Program, Step by Step

Each step tells you:
- **What** happens
- **Which variable** the result goes into (`variable_name`) and **in which later step** it's used
- **Why** this data type and not a different one

> Tip: put everything in **one** `.py` file, with one **function** per step (`def load_coordinates(...)`). That keeps it easy to read and easy to name for the submission.

---

## Overview of the important variables

| Variable | Data type | Contents | Created in step | Used in step |
|---|---|---|---|---|
| `TARGETS` | dict `{str: int}` | name → node ID of the 3 targets | 0 | 7, 9, 10, 11 |
| `coords` | list of tuples `(lat, lon)` | coordinates per node | 1 | 4, 10, A\* |
| `first_arc` | list of int | start line of each node in arclist | 2 | 3 |
| `arcs` | list of tuples | all arcs (one line = one tuple) | 2 | 3 |
| `graph` | list of lists of tuples | outgoing arcs per node | 3 | 6, 8 |
| `start_node` | int | your home node | 4 | 6, 7 |
| `cost` | list of float | cheapest known cost to each node | 6 | 9 |
| `pred` | list of int | predecessor of each node | 6 | 7, 8 |
| `results` | dict | path, time and length of each route | 8 | 9, 10 |

---

## Step 0 – Settings at the top of the file

1. Import the modules: `math`, `heapq`, `time`, `matplotlib.pyplot`.
2. Write the file paths into variables (`NODEPL_FILE = "data/nodepl.txt"`, …). If the folder changes, you only edit one line.
3. Store your home coordinates in `HOME = (47.0xxx, 15.4xxx)`. You can get them in Google Maps: right-click on your house and the coordinates appear at the top.
   - **Why a tuple?** Latitude and longitude always belong together and never change. A tuple is "read-only", so you can't overwrite one of them by accident.
4. Store the targets in a dictionary: `TARGETS = {"Basilika Mariatrost": 9328, "Schloss Eggenberg": 6031, "Murpark": 8543}`.
   - **Why a dict?** You want to look up "name → node". The names are also the labels in the plot legend later. A list would only give you numbers without names.
5. `ONEWAY_LIMIT = 1000` – arcs with a time above this count as forbidden (see trap 1 in `01_DATA_EXPLAINED.md`).

## Step 1 – Load the coordinates (`nodepl.txt`)

1. Create an empty list `coords` and immediately append `None` as a placeholder for index 0.
2. Open the file with `with open(NODEPL_FILE) as f:`. Then loop over the lines with `for line in f:`.
3. Split each line with `line.split()`. That gives you a list with 2 strings.
4. Turn both strings into floats with `float(...)`. Append them to `coords` as the tuple `(lat, lon)`.
5. Check: `len(coords)` must be **9505** (9504 nodes + placeholder). `coords[1]` must be `(47.0527089, 15.4404670)`.

- **Why an outer list (and not a dict)?** The node IDs are **consecutive numbers** 1…9504. A list index is exactly that, so `coords[node]` finds the value straight away. A dict with keys 1…9504 would work too, but it brings no benefit and uses more memory.
- **Why tuples inside?** A coordinate pair is a fixed unit and never changes (same as `HOME`).

## Step 2 – Load the pointers and the arcs (`nodelist.txt`, `arclist.txt`)

**2a – `first_arc`**
1. Create the list `first_arc = [None]` (placeholder at 0).
2. Loop over every line of `nodelist.txt` and append `int(line)`.
3. Check: `first_arc[1] == 1`, `first_arc[2] == 5`, `len(first_arc) == 9505`.

**2b – `arcs`**
1. Create the list `arcs = [None]` (placeholder at 0, so `arcs[1]` = line 1).
2. Loop over every line of `arclist.txt` and `split()` it into 6 parts.
3. Convert them: destination, clazz and flags with `int()`; time, distance and speed with `float()`.
4. Append the 6 values as **one tuple** `(dest, time_h, dist_km, speed, clazz, flags)`.
5. Check: `len(arcs) == 22341`.

- **Why a tuple per arc?** An arc is a fixed record of 6 values that belong together. You never want to change them. Tuples are also slightly faster and smaller than lists.
- 💡 Optional: to make it more readable, you can use `arc[0]`, `arc[1]` … or, even nicer, unpack it in the loop: `dest, t, d, v, clazz, flags = arc`.

## Step 3 – Build the graph (neighbour list)

This is where the adjacency list from slides 4 and 5 is turned into an easy-to-use structure.

1. Store the number of nodes: `N = len(first_arc) - 1` (= 9504).
2. Create `graph = [[]]`. Index 0 is an empty placeholder list.
3. Loop with `for node in range(1, N + 1):`
   - `start = first_arc[node]`
   - `end = first_arc[node + 1]` if `node < N`, otherwise `end = len(arcs)` (the last node, see `01_DATA_EXPLAINED.md`)
   - `graph.append(arcs[start:end])` – the slice `start:end` **excludes** `end`, which is exactly right here.
4. Check: `graph[1]` must contain 4 arcs with the destinations 2, 491, 7388 and 2323.

- **Why a list of lists?** The outer list again has "index = node ID". The inner list holds the outgoing arcs. A **list** fits here because every node has a **different number** of arcs and you only ever **loop over** them (`for arc in graph[u]`). You never search inside them.
- **Why not a dict `{node: [...]}`?** Same reason as in step 1: the IDs are consecutive, so a list is simpler.

## Step 4 – Find the start node (nearest to your home)

1. Set `best_node = None` and `best_d = math.inf` ("nothing found yet, infinitely far away").
2. Compute `cos_lat = math.cos(math.radians(HOME[0]))` once.
3. Loop over all nodes: `for node in range(1, N + 1):`
   - `dlat = coords[node][0] - HOME[0]`
   - `dlon = (coords[node][1] - HOME[1]) * cos_lat` ← the correction from trap 4
   - `d = math.sqrt(dlat**2 + dlon**2)`
   - If `d < best_d`: store `best_d = d` and `best_node = node`.
4. Store the result in `start_node = best_node` and print it. Check it: paste the coordinates `coords[start_node]` into Google Maps. Is that next to your house?
5. Optional: convert `best_d` to metres (× 111,000) and report it in the presentation ("the nearest node is 35 m from the front door").

- **Why two plain variables (`best_node`, `best_d`) instead of a list of all distances?** You only need the minimum. Storing 9504 values just to search through them again afterwards would be pointless.

## Step 5 – Cost functions

Write **small functions** that return the cost of one arc:

1. `cost_time(arc)`: if `arc[1] >= ONEWAY_LIMIT` → return `math.inf`. Otherwise return `arc[1]` (hours).
2. `cost_distance(arc)`: if `arc[1] >= ONEWAY_LIMIT` → `math.inf` (**important!**, trap 1). Otherwise return `arc[2]` (km).
3. (Later for 2.1: `cost_own(arc)`.)

- **Why functions instead of a column number?** In the next step, you pass the function to Dijkstra as a **parameter**: `dijkstra(graph, start_node, cost_time)`. You write Dijkstra **only once**, and it works with every cost. For 2.1 you just write another small function.

## Step 6 – Dijkstra

Write a function `dijkstra(graph, start, cost_function)` that returns `cost`, `pred` and `visited`.

**Preparation – four variables:**

| Variable | Initial value | Data type and **why** |
|---|---|---|
| `cost` | `[math.inf] * (N + 1)`, then `cost[start] = 0` | **List**: one value per node, accessed by node ID. `inf` means "not reached yet". |
| `pred` | `[0] * (N + 1)` | **List**: one predecessor per node. `0` means "none", because there is no node 0. |
| `visited` | `set()` | **Set**: the only question we ask it is "is node X already done?". A set answers that **instantly**. A list would have to compare every element (too slow with 9504 nodes). |
| `queue` | `[(0, start)]` | **List used as a heap** (with `heapq`): we always need the node with the **smallest** cost. A heap returns it quickly, without sorting everything. |

- **Why tuples `(cost, node)` in the queue?** `heapq` sorts tuples by their **first** element. So the cost has to come first. The tuple keeps the cost and the node together.

**The loop (in plain words):**

1. **While** `queue` is not empty:
2. Take out the cheapest entry: `c, u = heapq.heappop(queue)`.
3. **If** `u` is already in `visited` → `continue` (it's an old, outdated entry; see the note below).
4. Add `u` to `visited` (from now on, `cost[u]` is final).
5. **For** every `arc` in `graph[u]`:
   - `v = arc[0]` (destination node)
   - `w = cost_function(arc)` (cost of this arc)
   - If `w` is `math.inf` → `continue` (forbidden arc).
   - `new_cost = c + w`
   - **If** `new_cost < cost[v]`: we found a better way to `v`!
     - `cost[v] = new_cost`
     - `pred[v] = u` ← **this is the predecessor list**
     - `heapq.heappush(queue, (new_cost, v))`
6. At the end: `return cost, pred, visited`

> **Note on "outdated entries":** If a node gets a better cost, we just push it into the queue **again** and don't delete the old entry (Python's heap can't easily delete entries). Step 3 makes sure the old entry is ignored. This trick is called "lazy deletion".

> **Smart:** a **single** Dijkstra run (without stopping early) computes the cheapest route from the start to **all** nodes. So you get all 3 targets at once. You only need **2 runs** in total: time and distance.

**Testing (slide 9!) – before you use the Graz data:**

Build the small graph from the lecture by hand (directed arcs):
`1→2 (4), 1→3 (13), 1→4 (3), 2→3 (11), 2→5 (3), 4→3 (8), 4→5 (6), 5→3 (3)`.
Expected result from node 1:

| Node | cost | pred |
|---|---|---|
| 1 | 0 | – |
| 2 | 4 | 1 |
| 3 | **10** | 5 |
| 4 | 3 | 1 |
| 5 | 7 | 2 |

The cheapest path to 3 is 1 → 2 → 5 → 3 = 4 + 3 + 3 = 10. If your function produces this, it's correct.

## Step 7 – Save `prelist.txt` (hint from slide 10)

1. Open a file with `with open("prelist_time.txt", "w") as f:`.
2. Loop over `pred` from index 1 to N and write one value per line (line = node ID, the same format as the given files).
3. Do the same for `prelist_distance.txt`.

## Step 8 – Rebuild the path from `pred`

Write a function `get_path(pred, start, target)`:

1. `path = [target]`, `node = target`
2. **While** `node != start`:
   - `node = pred[node]`
   - If `node == 0` → the target is unreachable → `return None` (protection against an endless loop).
   - `path.append(node)`
3. `path.reverse()` (we walked backwards from the target to the start) → `return path`

- **Why a list?** A path has an **order** (first this node, then that one) and grows step by step with `append`. A set would lose the order, and a tuple can't grow.

**Compute time and length along the path** (for the comparison):
1. Write a function `path_stats(graph, path)`.
2. Set `total_time = 0` and `total_dist = 0`.
3. Loop over consecutive pairs: `for u, v in zip(path[:-1], path[1:]):`
4. Look in `graph[u]` for the arc whose `arc[0] == v`, and add its time and distance.
5. Return `total_time * 60` (minutes) and `total_dist` (km).

→ Why bother? A route that is optimal by **distance** also has a time, and the other way round. That's exactly what the comparison is about.

**Save everything in `results`:**

```
results[("time", "Murpark")] = {"path": [...], "time_min": 12.3, "dist_km": 8.1, "n_nodes": 57}
```

- **Why a dict with tuple keys?** You want to look up "which cost, which target" by **meaning**, not by an index you have to remember. The key has to be a **tuple** because dict keys must not be changeable, so lists are not allowed as keys.
- **Why a dict as the value?** The values have **names** (`"time_min"`), which is easier to read than `values[2]`.

## Step 9 – Comparison (table)

1. Loop over `TARGETS` and over the two costs `"time"` and `"distance"`.
2. For each route, print one row: target | optimized for | time [min] | length [km] | number of nodes.
3. Interpretation for the presentation, for example: *"The time-optimal route to Murpark is 1.8 km longer but 3 minutes faster, because it uses the faster main road (clazz 15) instead of residential streets (clazz 41)."*
   - 💡 Tip: you can also count which `clazz` values a route uses. Time routes like main roads, distance routes like side streets.

## Step 10 – Visualization (matplotlib)

1. `fig, ax = plt.subplots(figsize=(10, 8))`
2. **Background network (optional, but looks good):** draw all arcs in light grey and thin (`linewidth=0.3`).
   - Plain version: loop over all nodes `u` and all `arc` in `graph[u]`, and use `ax.plot([lon_u, lon_v], [lat_u, lat_v], ...)`. That is **slow** with 22,000 lines.
   - Faster: collect all line pieces in a list and draw them in one go with `matplotlib.collections.LineCollection`.
3. **Draw each route:** build the lists `lons = [coords[n][1] for n in path]` and `lats = [coords[n][0] for n in path]` → `ax.plot(lons, lats, linewidth=2.5, label="Time – Murpark")`.
   - Example: time = solid line, distance = dashed (`linestyle="--"`), one colour per target.
4. **Markers:** the start as a big marker (e.g. a star) and the targets with `ax.annotate(name, ...)`.
5. **Labels (required according to the PDF):** `ax.set_xlabel("Longitude λ [°]")`, `ax.set_ylabel("Latitude φ [°]")`, `ax.set_title(...)`, `ax.legend()`.
6. **Aspect ratio (slide 10!):** `ax.set_aspect(1 / math.cos(math.radians(47.07)))` – this way 1 km east looks as long as 1 km north on the map. Without it, Graz looks squashed.
7. Save: `fig.savefig("routes_time_distance.png", dpi=300)` → straight into the slides.
8. Optional: a background map with `contextily` (it needs the coordinates in Web Mercator, so it's a bit fiddly – leave it for the end).

## Step 11 – The extra task

→ See `03_OPTION_A_STAR_OR_COST_FUNCTION.md`.

## Step 12 – Wrapping up

1. `main()` function: call steps 1–11 in order. At the end of the file: `if __name__ == "__main__": main()`.
2. Measure the runtime with `time.perf_counter()` (it goes in the README).
3. Write comments: one short sentence above each function (what goes in, what comes out) and comments on the non-obvious lines (the one-way limit, the placeholder at index 0, lazy deletion).
4. `README.txt`: Python version (`python --version`), required packages, runtime, and what happens if the data folder is missing.
5. ZIP: `.py` + `README.txt` + `data/`.
