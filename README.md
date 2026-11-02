# Navigation Systems 2026/27 – Lab 1: Routing

Shortest-path routing in the street network of Graz with **Dijkstra** (cost = time and cost = distance)
and **A\*** (cost = distance, extra task 2.2).

Group: Breitler, Stering

## Contents

| File | Description |
|---|---|
| `Assigment_01_BREITLER_STERING.py` | The program: loads the data, finds the start node, runs Dijkstra and A*, saves the predecessor lists and plots |
| `00_PLAN.md` | Overall plan and what has to be handed in |
| `01_DATA_EXPLAINED.md` | How the three data files work |
| `02_PROGRAM_STEP_BY_STEP.md` | The program, step by step |
| `data/nodepl.txt` | Coordinates (lat, lon) of every node |
| `data/nodelist.txt` | For every node the row in `arclist.txt` where its arcs start |
| `data/arclist.txt` | The arcs: destination, travel time [h], length [km], speed limit, class, flags |

## What the program does

1. Loads the three data files (with a placeholder at index 0, because the node ids start at 1).
2. Finds the start node: the node closest to our home (haversine distance).
3. **Task 1:** Dijkstra from the start node to the three targets, once with time and once with distance as cost:
   - Basilika Mariatrost → node 9328
   - Schloss Eggenberg → node 6031
   - Murpark → node 8543
4. **Task 2.2:** A* with the straight-line distance as heuristic, compared with Dijkstra (visited nodes and runtime).
5. One-way streets in the wrong direction (travel time above `oneway_limit`) are skipped.

## Output

- `prelist_time_<node>.txt`, `prelist_distance_<node>.txt` – predecessor lists (row = node id, value = predecessor, 0 = none)
- `dijkstra_time_distance.png` – all routes, time (solid) vs. distance (dashed)
- `dijkstra_vs_astar_<node>.png` – searched streets of Dijkstra vs. A* for each target

## Results

| Target | Time-optimal | Distance-optimal | Visited nodes (Dijkstra / A*) |
|---|---|---|---|
| Basilika Mariatrost | 3.67 km, 4.7 min | 3.67 km, 4.7 min | 1829 / 122 |
| Schloss Eggenberg | 7.45 km, 9.4 min | 7.12 km, 10.6 min | 6135 / 1354 |
| Murpark | 6.63 km, 8.4 min | 6.17 km, 9.5 min | 4964 / 899 |

## Requirements and how to run

- Python 3.14 (tested with 3.14.7)
- matplotlib (tested with 3.11.2)

```bash
pip install matplotlib
python Assigment_01_BREITLER_STERING.py
```

Total runtime: about 3.5 s (most of it is plotting; each routing takes only a few ms).

## Possible errors

- **`FileNotFoundError`**: the paths to the data files are set at the top of the script (section *Files*).
  Change them so they point to the `data/` folder on your computer.
- **`ModuleNotFoundError: No module named 'matplotlib'`**: install matplotlib (see above).
