# Video Script – Lab 1 Routing (max. 5:00)

**Speakers:** **A** = Breitler, **B** = Stering
**Target length:** about 4:45 (≈ 700 spoken words at a calm pace), so there is a buffer to the 5:00 limit.
**Format:** PowerPoint with recorded audio → export as `.mp4` → name it after the group, e.g. `GroupX.mp4`.

Sentences in *[square brackets and italics]* are **optional**. Cut them first if a test recording is over 4:50.

---

## Overview

| # | Slide | Speaker | Time | Length |
|---|---|---|---|---|
| 1 | Title | A | 0:00 – 0:15 | 15 s |
| 2 | The data | A | 0:15 – 1:00 | 45 s |
| 3 | Start node | A | 1:00 – 1:20 | 20 s |
| 4 | Dijkstra – how it works | B | 1:20 – 2:00 | 40 s |
| 5 | Results: time vs. distance | B | 2:00 – 2:50 | 50 s |
| 6 | A\* – how it works | A | 2:50 – 3:30 | 40 s |
| 7 | Results: Dijkstra vs. A\* | B | 3:30 – 4:05 | 35 s |
| 8 | Pros and cons of A\* | A | 4:05 – 4:35 | 30 s |
| 9 | Conclusion | B | 4:35 – 4:50 | 15 s |

---

## Slide 1 – Title (A, 0:00 – 0:15)

**On the slide:**
- Navigation Systems 2026/27 – Lab 1: Routing
- Group X – Breitler, Stering
- Small map of Graz in the background (crop of `dijkstra_time_distance.png`)

**Spoken (A):**
> Hello, we are group X, [first name] Breitler and [first name] Stering. In this video we present our first lab programme: optimal routes through the street network of Graz with Dijkstra's algorithm, and as our extra task, the A-star algorithm.

---

## Slide 2 – The data (A, 0:15 – 1:00)

**On the slide:**
- Diagram of the adjacency list: `nodelist` → row in `arclist` (like slide 4 of the lecture), with node 1 as example: rows 1–4 → 4 arcs
- `nodepl.txt`: 9504 nodes (φ, λ)
- `arclist.txt`: 22,340 arcs: destination | time [h] | length [km] | speed | clazz | flags
- Two boxes: "Index 0 = placeholder" and "One-way: time = 1,000,000 h → skip"

**Spoken (A):**
> The network is given as an adjacency list in three text files. nodepl holds the coordinates of 9504 nodes. nodelist tells us for every node in which row of the arclist its outgoing arcs start. And the arclist holds 22,340 arcs, each with destination node, travel time, length, speed limit, road class and flags.
>
> Two details were important. First, the files count from one, but Python counts from zero, so every list gets a placeholder at index zero. Second, one-way streets: in the wrong direction the travel time is one million hours, but the length is normal. So we skip every arc with a time above 1000. *[Otherwise our distance routes would drive the wrong way down one-way streets.]*

---

## Slide 3 – Start node (A, 1:00 – 1:20)

**On the slide:**
- Haversine formula (the sin² form)
- Source: GeoMathe 1, "Sphärischer Cosinussatz für Seiten – numerisch stabile Alternative"
- Result: **start node 6386, 75 m from home** (map crop with home and start node)

**Spoken (A):**
> To find our start node, we compute the distance from our home to every node with the haversine formula, and keep the closest one. *[It's the numerically stable form of the spherical law of cosines, which is more precise for short distances.]* Our start node is node 6386, 75 metres from home.

---

## Slide 4 – Dijkstra: how it works (B, 1:20 – 2:00)

**On the slide:** the loop as 4 short steps (maybe with a small flow chart):
1. Take the open node with the **smallest cost** (priority queue, `heapq`)
2. Its cost is now **final**
3. For every outgoing arc: cheaper way to the neighbour? → new cost + **predecessor**
4. Goal reached → walk back through the **predecessor list** → route

- Cost = one column of the arclist: **time [h]** or **distance [km]**

**Spoken (B):**
> Dijkstra starts at this node with cost zero. In every step it takes the open node with the smallest cost, using a priority queue, and that cost is now final. Then it looks at all outgoing arcs. If the way over the current node is cheaper, the neighbour gets the new cost, and the current node is stored as its predecessor. When the goal is reached, we walk back through the predecessor list and get the route. *[We also save these predecessor lists as text files.]* The cost is just one column of the arclist, time or distance. The algorithm stays the same.

---

## Slide 5 – Results: time vs. distance (B, 2:00 – 2:50)

**On the slide:**
- `dijkstra_time_distance.png` (large, solid = time, dashed = distance)
- Table:

| Target | Optimised for time | Optimised for distance |
|---|---|---|
| Basilika Mariatrost | 3.67 km, 4.7 min | 3.67 km, 4.7 min (same route) |
| Schloss Eggenberg | 7.45 km, **9.4 min** | **7.12 km**, 10.6 min |
| Murpark | 6.63 km, **8.4 min** | **6.17 km**, 9.5 min |

- Small note: residential streets (clazz 41) on the way to Eggenberg: time route 0.4 km, distance route 3.1 km

**Spoken (B):**
> Here are our six routes. Solid lines are optimised for time, dashed lines for distance.
>
> To Basilika Mariatrost, both routes are identical: 3.67 kilometres and 4.7 minutes, almost all of it on one primary road.
>
> To Schloss Eggenberg, the shortest route is 7.12 kilometres but takes 10.6 minutes. The fastest route is 330 metres longer, but more than a minute faster. Murpark shows the same: the fastest route is about 460 metres longer, but also about a minute faster.
>
> The reason: the distance route takes the direct way through residential streets, about three kilometres of them on the way to Eggenberg. The time route avoids them and uses primary and secondary roads with higher speed limits, so the detour pays off.

---

## Slide 6 – A\*: how it works (A, 2:50 – 3:30)

**On the slide:**
- Dijkstra: priority = **cost so far**
- A\*: priority = **cost so far + estimate to the goal**
- Estimate h = straight-line (haversine) distance to the goal
- "Road ≥ straight line → h never overestimates → A\* stays optimal"
- The two code lines side by side:
  ```python
  value = new_cost                                                       # Dijkstra
  value = new_cost + haversine(coordinates[neighbour], coordinates[goal]) # A*
  ```

**Spoken (A):**
> For our extra task we implemented A-star. Dijkstra spreads out evenly in all directions. A-star adds an estimate of the remaining cost, so it searches towards the goal. We use distance as cost, and the straight-line haversine distance to the goal as the estimate. A road can never be shorter than the straight line, so the estimate never overestimates, and A-star still finds the optimal route. In our code, Dijkstra and A-star are the same function. The only difference is the priority in the queue: cost plus estimate, instead of just the cost.

---

## Slide 7 – Results: Dijkstra vs. A\* (B, 3:30 – 4:05)

**On the slide:**
- `dijkstra_vs_astar_6031.png` (Schloss Eggenberg: left Dijkstra, right A\*)
- Table:

| Target | Route length (both) | Visited nodes Dijkstra / A\* | Runtime Dijkstra / A\* |
|---|---|---|---|
| Basilika Mariatrost | 3.666 km | 1829 / 122 | ≈ 1.2 / 0.2 ms |
| Schloss Eggenberg | 7.115 km | 6135 / 1354 | ≈ 6.6 / 2.9 ms |
| Murpark | 6.167 km | 4964 / 899 | ≈ 5.3 / 1.8 ms |

> ⚠️ Run the script once more right before recording and copy the runtimes from that run. They change a little every time.

**Spoken (B):**
> On the left you see the streets Dijkstra searched on the way to Schloss Eggenberg, on the right the ones A-star searched. Both find exactly the same route, 7.115 kilometres. But Dijkstra visited over 6000 nodes, A-star only about 1350. For all three targets, A-star visits only 7 to 22 percent of the nodes, and is about two to six times faster.

---

## Slide 8 – Pros and cons of A\* (A, 4:05 – 4:35)

**On the slide:**

| ✅ Pros of A\* | ❌ Cons of A\* |
|---|---|
| Visits far fewer nodes | Needs a good heuristic (coordinates) |
| Faster for one start → one goal | Weaker estimate for time as cost (÷ max. speed 120 km/h) |
| Still optimal if h never overestimates | One run per goal, while one full Dijkstra run reaches all goals |

**Spoken (A):**
> So what are the pros and cons? A-star visits far fewer nodes, is faster for one start and one goal, and still finds the optimal route, as long as the estimate never overestimates. On the other hand, it needs a good heuristic, so it needs coordinates. With time as cost, the estimate would be weaker, because we'd have to divide by the maximum speed. And A-star needs one run per goal. For routes from one start to many goals, one full Dijkstra run gives you all of them at once.

---

## Slide 9 – Conclusion (B, 4:35 – 4:50)

**On the slide:**
- Time vs. distance: different routes whenever a faster road is worth a detour
- A\*: same optimal routes, a fraction of the work
- Thank you!

**Spoken (B):**
> To sum up: time and distance give different routes whenever a faster road is worth a detour. And A-star finds the same optimal routes as Dijkstra with a fraction of the work. Thanks for watching!

---

## Checklist: does the video cover the assignment?

| Requirement (assignment PDF) | Where in the video |
|---|---|
| Methodology | Slides 2, 3, 4, 6 |
| Visualization of the routes with time and distance as costs | Slide 5 |
| Comparison of these routes | Slide 5 |
| Visualization of the routes of A\* and Dijkstra in a map | Slide 7 |
| Comparison and interpretation of both algorithms | Slide 7 |
| Explanation of the implementation of A\* | Slide 6 |
| Pros and cons of A\* over Dijkstra | Slide 8 |
| Maps with labels, units, correct scale | All plots: axes in °, aspect ratio corrected |
| Both voices, ≤ 5 min, `.mp4`, named after the group | Recording, see below |

## Recording tips

- **Before recording:** run the script once more, copy the runtimes into slide 7, and fill in the group number on slide 1 and in the file name.
- **PowerPoint:** *Slide Show → Record*. Each person can record their own slides. Then *File → Export → Create a Video* → `.mp4`.
- **Test run:** read the whole script once with a stopwatch. If it's over 4:50, cut the *[optional]* sentences.
- **Plots on the slides:** use the PNGs at full width. The street network is fine, so a small picture becomes unreadable.
