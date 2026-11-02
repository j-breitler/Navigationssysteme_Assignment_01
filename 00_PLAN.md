# Lab 1 – Routing: Overall Plan

Read the files in this order:

| File | What it covers |
|---|---|
| `00_PLAN.md` (this file) | What you have to hand in, the big picture, and a timeline |
| `01_DATA_EXPLAINED.md` | How the three `.txt` files work and the traps hidden in them |
| `02_PROGRAM_STEP_BY_STEP.md` | The program, step by step, with the reason for each data type |
| `03_OPTION_A_STAR_OR_COST_FUNCTION.md` | The extra task: A* (2.2) or your own cost function (2.1) |

---

## 1. What the assignment asks for (summary)

1. **Find your start node:** take the home address of someone in your group and find the node in `nodepl.txt` that is closest to it.
2. **Run Dijkstra** from this start node to three targets:
   - Basilika Mariatrost → node **9328**
   - Schloss Eggenberg → node **6031**
   - Shopping-Center Murpark → node **8543**
3. Do this **twice**: once with **time** as the cost and once with **distance** as the cost. That gives 3 targets × 2 costs = 6 routes.
4. **Pick one extra task:**
   - **2.1** Make up your own cost function, route with it, and compare it with time and distance.
   - **2.2** Write **A\*** as well, calculate the 3 routes with it (time *or* distance is enough), and compare it with Dijkstra.
5. **Visualize** the routes on a map with axis labels, units, the right aspect ratio and sensible line widths. The slides say to store the predecessor list in a file (`prelist.txt`).
6. **Hand in by 22 November, 23:59** (that's 20 days from today, 2 Nov):
   - a ZIP containing `lab01_ws2026_27_GROUP#_SURNAME1_SURNAME2.py`, a `README.txt` (Python version, runtime, possible errors) and the `data/` folder
   - a video of at most 5 minutes (`.mp4`, with your voice) named after your group, e.g. `GroupA.mp4`

## 2. The program at a glance

```
 ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐   ┌──────────────┐   ┌────────────┐
 │ 1. Load the  │ → │ 2. Build the │ → │ 3. Find the start│ → │ 4. Dijkstra  │ → │ 5. Rebuild │
 │ 3 txt files  │   │ graph        │   │ node (nearest to │   │ (time, dist) │   │ the paths  │
 │              │   │ (neighbours) │   │ your home)       │   │ → cost, pred │   │ from pred  │
 └──────────────┘   └──────────────┘   └──────────────────┘   └──────────────┘   └─────┬──────┘
                                                                                       ↓
                       ┌────────────────────┐   ┌──────────────────────────┐   ┌──────────────┐
                       │ 8. Video + README  │ ← │ 7. Extra: A* or your own │ ← │ 6. Plot and  │
                       │ + ZIP              │   │ cost function            │   │ compare      │
                       └────────────────────┘   └──────────────────────────┘   └──────────────┘
```

## 3. Which extra task? My recommendation

**For a Python beginner I recommend 2.2 (A\*).** Here's why:

- A\* is Dijkstra with about 5 changed lines. Once Dijkstra works, A\* is quick to add.
- The comparison is easy to measure: "Dijkstra visited 6,000 nodes and A\* visited 900, and both found the same route." A plot of the visited nodes makes a strong slide.
- In 2.1 you have to *invent* something and *argue* that it makes sense, so the presentation needs more creativity. It's the better choice if you want to compete for the "best presentation award".

Both options are described in `03_OPTION_A_STAR_OR_COST_FUNCTION.md`.

## 4. Suggested timeline

| When | Goal |
|---|---|
| **Week 1 (2–8 Nov)** | Load the data, build the graph, test Dijkstra on the small example from the lecture (slide 9), then run it on Graz |
| **Week 2 (9–15 Nov)** | Rebuild the paths, make the plots, write the comparison table, build the extra task (A\* or cost function) |
| **Week 3 (16–22 Nov)** | Make the slides, record the video (≤ 5 min), write the README, clean up the comments, build the ZIP. **Leave 2 days as a buffer.** |

## 5. Tools you'll need (Python)

| Module | Used for | Install? |
|---|---|---|
| `math` | `inf`, `cos`, `radians`, `sqrt`, `sin`, `atan2` | built-in |
| `heapq` | Priority queue for Dijkstra/A\* | built-in |
| `time` | Measuring runtime (`time.perf_counter()`) | built-in |
| `matplotlib` | Drawing the map/routes | `pip install matplotlib` |
| `numpy` (optional) | Faster loading with `numpy.loadtxt` | `pip install numpy` |
| `contextily` (optional) | Background map tiles (OpenStreetMap) | `pip install contextily` |
