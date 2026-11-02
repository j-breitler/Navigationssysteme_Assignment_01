# The Data Explained

There are three files in `data/`. **Each line of a file is one entry, and the line number is the ID.** Line numbers start at **1**, but Python counts from **0**. Keep that in mind; there's more on it below.

---

## 1. `nodepl.txt` – coordinates of the nodes (9504 lines)

```
line 1:    47.0527089     15.4404670     ← node 1:  φ (latitude) = 47.05°, λ (longitude) = 15.44°
line 2:    47.0530285     15.4411845     ← node 2
...
```

- Column 1 = **latitude φ** [°] (north–south, the y-axis on the map)
- Column 2 = **longitude λ** [°] (east–west, the x-axis on the map)
- ⚠️ When you plot, use **x = longitude, y = latitude**. Mixing them up is a very common mistake.

## 2. `nodelist.txt` – where each node's arcs start (9504 lines)

```
line 1:  1      ← node 1's arcs start at line 1 of arclist.txt
line 2:  5      ← node 2's arcs start at line 5
line 3:  7      ← node 3's arcs start at line 7
line 4:  9
...
line 9504: 22341
```

**Important:** the assignment PDF says the file contains "outgoing valences", but the numbers are actually **pointers (start lines)** into `arclist.txt`. The **valence** (number of outgoing arcs) is the **difference** between two neighbouring values. This is exactly what slide 4 shows (1, 6, 9, 12, 15 → 5, 3, 3, 3 arcs).

> Node `i` owns the lines `nodelist[i]` up to `nodelist[i+1] − 1` of `arclist.txt`.
>
> Example: node 1 → lines 1, 2, 3, 4 (because node 2 starts at 5) → 4 outgoing arcs.

**The last node (9504):** there is no "next" line. Use "up to the end of arclist" instead. `arclist.txt` has 22340 lines, and `nodelist[9504] = 22341`, so node 9504 has **0** outgoing arcs. That's fine; your code only has to avoid crashing on it.

## 3. `arclist.txt` – the arcs (road segments) (22340 lines)

```
     2       0.002166  0.064976    30    31     7
  dest       time[h]   dist[km]  speed  clazz  flags
```

| Column | Meaning | Unit | Type in Python |
|---|---|---|---|
| 1 | destination node (where the road goes) | node ID | `int` |
| 2 | travel time | **hours** | `float` |
| 3 | length | **kilometres** | `float` |
| 4 | speed limit | km/h | `int`/`float` |
| 5 | clazz (road type, see the table in the assignment) | – | `int` |
| 6 | flags (who may use it) | – | `int` |

The **start** node of an arc is not in the line itself. It follows from `nodelist`: whichever node "owns" that line is the start.

**Example, worked out by hand (node 1):**

| arclist line | from | to | time [h] | dist [km] |
|---|---|---|---|---|
| 1 | 1 | 2 | 0.002166 | 0.064976 |
| 2 | 1 | 491 | 0.003460 | 0.103788 |
| 3 | 1 | 7388 | 0.001744 | 0.052305 |
| 4 | 1 | 2323 | 0.003568 | 0.107041 |

Use this table later to check your graph: `graph[1]` must contain exactly these 4 arcs.

---

## ⚠️ Traps I found in the data

### Trap 1: One-way streets only show up in the TIME column

- An arc that goes **against** a one-way street has `time = 1000000` h. (The PDF says 100000, but the data contains **1000000**.) 2038 arcs have this value.
- The **distance column is normal** for these arcs!
- → When you route by **distance**, you would happily drive the wrong way down one-way streets, unless you check in your distance cost function: *"if the time is ≥ 1000, this arc is forbidden"*.
- For routing by time it "works by itself" because 1,000,000 h is never the cheapest option. Still, it's cleaner to skip those arcs there as well.

### Trap 2: Python indexes from 0, the files from 1

- Node 1 is on line 1, but in a Python list it would be at index 0.
- **My suggestion:** put a **dummy element at index 0** of every list (e.g. `None`). Then `coords[1]` really is node 1, `arcs[1]` really is arclist line 1, and you never need `-1` or `+1` anywhere. That removes a whole class of bugs.
- A side bonus: the value `0` is free and can mean "no predecessor" (no node has ID 0).

### Trap 3: Units

- Time is in **hours**. For the presentation, convert to **minutes** (× 60).
- Distance is in **km**.
- I checked it: time = distance / speed holds for every arc (except the one-way arcs).

### Trap 4: Units of the coordinate difference

- 1° of latitude ≈ 111 km, but 1° of longitude in Graz is only ≈ 111 km × cos(47°) ≈ 76 km.
- So when you search for the nearest node, you should multiply Δλ by cos(φ). Otherwise the east–west direction gets the wrong weight. (It's a small effect, but it's correct this way and is nice to mention in the presentation.)

### Not a trap, just useful

- **Flags:** all arcs have flag 1, 3, 5 or 7, so **every arc may be driven by car**. There are no pure bike or pedestrian arcs. You can therefore ignore the flags for the car routes. They're only interesting for your own cost function (2.1).
- **Highest speed in the data: 120 km/h.** You'll need this for the A\* heuristic with time as the cost.
